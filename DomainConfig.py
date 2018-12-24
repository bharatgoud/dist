import json

class Domain:
    def __init__(self, domain_name=None, domain_config_location=None, domain_version=None):
        self.domain_name = domain_name
        self.domain_config_location = domain_config_location
        self.domain_version = domain_version
        self.servers = []
        self.clusters = []
        self.applications = []
        self.datasources = []
        self.jmsresources = []

    def add_server(self, server):
        self.servers.append(server)
        
    def add_cluster(self, cluster):
        self.clusters.append(cluster)
    
    def add_application(self, application):
        self.applications.append(application)
    
    def add_datasource(self, datasource):
        self.datasources.append(datasource)
    
    def add_jmsresource(self, jmsresource):
        self.jmsresources.append(jmsresource)
    
    def to_json(self):
        return json.dumps(self.__dict__)
    
    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)
        

class Server:
    def __init__(self, server_name=None, listen_port=None, server_cluster=None):
        self.server_name = server_name
        self.listen_port = listen_port
        self.server_cluster = server_cluster
        
        

class Cluster:
    def __init__(self, cluster_name=None):
        self.cluster_name = cluster_name
        
        
class Application:
    def __init__(self, app_name=None, target_servers=None, module_type=None, app_path=None ):
         self.app_name = app_name
         self.target_servers = target_servers
         self.module_type = module_type
         self.app_path = app_path
         
         
class Datasource:
    def __init__(self, datasource_name=None, target_server=None, datasource_location=None, jdbc_url=None,jndi_name=None):
         self.datasource_name = datasource_name
         self.target_server = target_server
         self.datasource_location = datasource_location
         self.jdbc_url = jdbc_url
         self.jndi_name = jndi_name
         
class Jmsresource:
    def __init__(self, jmsresource_name=None, target_server=None, subdeploy_name=None, subdeploy_target=None,jmsresource_location=None ):
            self.jmsresource_name = jmsresource_name
            self.target_server = target_server
            self.subdeploy_name = subdeploy_name
            self.subdeploy_target = subdeploy_target
            self.jmsresource_location = jmsresource_location
            self.jmsqueues = []
            self.jmstopics = []
            
    def add_jmstopic(self, jmstopic):
        self.jmstopics.append(jmstopic)
    
    def add_jmsqueue(self, jmsqueue):
        self.jmsqueues.append(jmsqueue)
            

class Jmsqueue:
    def __init__(self, jmsqueue_name=None, jmsqueue_sub_deploy_name=None, jmsqueue_jndi_name=None):
        self.jmsqueue_name = jmsqueue_name
        self.jmsqueue_sub_deploy_name = jmsqueue_sub_deploy_name  
        self.jmsqueue_jndi_name = jmsqueue_jndi_name
        

class Jmstopic:
    def __init__(self, jmstopic_name=None, jmstopic_jndi_name=None):
        self.jmstopic_name = jmstopic_name
        self.jmstopic_jndi_name = jmstopic_jndi_name
