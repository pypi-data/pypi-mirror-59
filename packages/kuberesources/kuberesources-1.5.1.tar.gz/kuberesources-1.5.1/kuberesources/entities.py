from .helpers import Parsers, Kube
from kubernetes.client.rest import ApiException
from kubernetes import client
from colorama import Fore, Style
from prettytable import PrettyTable

class KubeResources:
    def __init__(self, kubeClient : Kube):
        self.__kubeClient = kubeClient
        self.__getNodeData()
    
    def __getNodeData(self):
        allData = []
        try:
            nodes = self.__kubeClient.api.list_node(label_selector='!node-role.kubernetes.io/master')
            for node in nodes.items:            
                nodeName = node.metadata.name
                nodeData = NodeData(nodeName, node.status.capacity)
                pod_templates = self.__kubeClient.api.list_pod_for_all_namespaces(field_selector='spec.nodeName=%s,status.phase!=Failed,status.phase!=Succeeded' % nodeName)
                
                for template in pod_templates.items:
                    name = template.metadata.name
                    
                    requests = self.__parseResourceRequestsForAllContainers(template.spec.containers)
                    nodeData.addCpuRequest(name, requests["cpu"])
                    nodeData.addMemRequest(name, requests["mem"])

                    limits = self.__parseResourceLimitsForAllContainers(template.spec.containers)
                    nodeData.addCpuLimit(name, limits["cpu"])
                    nodeData.addMemLimit(name, limits["mem"])

                allData.append(nodeData)
            self.__nodeData = allData
        except ApiException as e:
            print("Error when attempting to read node data: %s\n" % e)            

    def __parseResourceRequestsForAllContainers(self, containers):
        cpuRequests = 0
        memRequests = 0

        for container in containers:    
            if container.resources is None or container.resources.requests is None:
                continue
        
            requests = container.resources.requests
            if "cpu" in requests:
                cpuRequests += Parsers.parseCpuResourceValue(requests["cpu"])
            if "memory" in requests:
                memRequests += Parsers.parseMemoryResourceValue(requests["memory"])
        
        return {"cpu": cpuRequests, "mem": memRequests}

    def __parseResourceLimitsForAllContainers(self, containers):
        cpuLimits = 0
        memLimits = 0

        for container in containers:    
            if container.resources is None or container.resources.limits is None:
                continue
        
            limits = container.resources.limits
            if "cpu" in limits:
                cpuLimits += Parsers.parseCpuResourceValue(limits["cpu"])
            if "memory" in limits:
                memLimits += Parsers.parseMemoryResourceValue(limits["memory"])
        
        return {"cpu": cpuLimits, "mem": memLimits}

    def __printProgressBar(self, current, total, prefix="", suffix="", decimals=1, length=25, fill='#', printEnd="\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (current / float(total)))
        filledLength = int(length * current / total)
        if filledLength > length:
            color = Fore.RED
        elif filledLength < length/2:
            color = Fore.GREEN
        elif filledLength > length/2:
            color = Fore.YELLOW

        bar = color + fill * filledLength + Style.RESET_ALL + "-" * (length - filledLength)

        return "{} |{}| {}% {}".format(prefix, bar, percent, suffix)
            
    def print(self):
        print(Fore.GREEN + "Active kube context: {}".format(self.__kubeClient.context) + Style.RESET_ALL)
        table = PrettyTable(["Node", "CPU", "Memory"])
        table.align["Node"] = "l"
        table.align["CPU"] = "l"
        table.align["Memory"] = "l"

        for node in self.__nodeData:
            table.add_row([Fore.CYAN + node.name + Style.RESET_ALL, self.__printProgressBar(node.totalCpuRequests, node.cpuCapacity, "Req"), self.__printProgressBar(node.totalMemRequests, node.memCapacity, "Req")])
            table.add_row(['', self.__printProgressBar(node.totalCpuLimits, node.cpuCapacity, "Lim"), self.__printProgressBar(node.totalMemLimits, node.memCapacity, "Lim")])
            
            if self.__kubeClient.showPodInfo:
                for pod in node.cpuRequests.keys():
                    if node.cpuRequests[pod] == 0:
                        continue
                    table.add_row(["{}...".format(pod[0:14]), "{:>10}m / {:>5}m".format(node.cpuRequests[pod], node.cpuLimits[pod]), "{:>10}Mi / {:>5}Mi".format(int(node.memRequests[pod] / 1048576), int(node.memLimits[pod] / 1048576))])
        table.add_row(['','',''])
        table.add_row([Fore.CYAN + "Cluster total" + Style.RESET_ALL, self.__printProgressBar(NodeData.totalCpuRequests, NodeData.totalCpuCapacity, "Req"), self.__printProgressBar(NodeData.totalMemRequests, NodeData.totalMemCapacity, "Req")])
        print(table)

class NodeData:
    totalCpuRequests = 0
    totalCpuLimits = 0
    totalMemRequests = 0
    totalMemLimits = 0
    totalCpuCapacity = 0
    totalMemCapacity = 0

    def __init__(self, nodename, capacity):
        self.cpuRequests = {}
        self.memRequests = {}
        self.cpuLimits = {}
        self.memLimits = {}
        self.name = nodename
        self.cpuCapacity = int(capacity["cpu"]) * 1000
        self.memCapacity = Parsers.parseMemoryResourceValue(capacity["memory"])
        self.totalCpuRequests = 0
        self.totalMemRequests = 0
        self.totalCpuLimits = 0
        self.totalMemLimits = 0

        NodeData.totalCpuCapacity += self.cpuCapacity
        NodeData.totalMemCapacity += self.memCapacity

    def addCpuRequest(self, podName, cpuRequest):
        NodeData.totalCpuRequests += cpuRequest
        self.totalCpuRequests += cpuRequest
        self.cpuRequests[podName] = cpuRequest
    
    def addCpuLimit(self, podName, cpuLimit):
        NodeData.totalCpuLimits += cpuLimit
        self.totalCpuLimits += cpuLimit
        self.cpuLimits[podName] = cpuLimit

    def addMemRequest(self, podName, memRequest):
        NodeData.totalMemRequests += memRequest
        self.totalMemRequests += memRequest
        self.memRequests[podName] = memRequest

    def addMemLimit(self, podName, memLimit):
        NodeData.totalMemLimits += memLimit
        self.totalMemLimits += memLimit
        self.memLimits[podName] = memLimit
