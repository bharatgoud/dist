import xml.etree.ElementTree as ET
import traceback
import json
from DomainConfig import Domain
import DomainConfig as domain_cfg
#import jsonpickle.unpickler as unpickler

filepath = "/apps/opt/weblogic/weblogic103mp6/domain-registry.xml"


root = None
try:
    tree = ET.parse(filepath)
    root = tree.getroot()
except FileNotFoundError:
    print "@@@  Either file path is wrong or File is not avaliable at {0} ".format(filepath)


ns = {'domain-reg': 'http://xmlns.oracle.com/weblogic/domain-registry'}

domain_locations = dict()

if root is not None:
 try:
    print "+++++++ Parsing domain if available: +++++++++++++"
    """
    domain-registry has no.of domains, iterating each domain.
    """
    for domain in root.findall('domain-reg:domain', ns):
            domain_location = domain.get('location')
            domain_name = domain_location[domain_location.rfind('\\')+1:]
            domain_locations.update( {domain_name : domain_location.replace('\\\\', '\\')} )
            print domain_name +"----- "+ domain_location

    cns = {'domain_config': 'http://xmlns.oracle.com/weblogic/domain'}
    """
    each domain has the config file. parsing the config file.
    """
    domain_config_list = list()
    for domain_name, domain_location in domain_locations.items():
        domain = domain_cfg.Domain()
        domain.domain_name = domain_name

        config_location = domain_location+"/config/config.xml"
        domain.domain_config_location = config_location

        print " ***************  Domain Name:  {0} -- configuration details: ***************".format(domain_name)
        config_tree = ET.parse(config_location)
        config_root = config_tree.getroot()

        domain_version = config_root.find('domain_config:domain-version',cns)
        if domain_version is not None:
                print "domain_version : "+domain_version.text
                domain.domain_version = domain_version.text
        """
         Identifying the server details
        """
        servers = config_root.findall('domain_config:server', cns)
        print " --------------  servers: --------------"
        if servers:
            for server in servers:
                serverObj = domain_cfg.Server()
                server_name = server.find('domain_config:name', cns)
                if server_name is not None:
                     print "server_name : "+server_name.text
                     serverObj.server_name = server_name.text

                listen_port = server.find('domain_config:listen-port', cns)
                if listen_port is not None:
                     print "listen_port : "+listen_port.text
                     serverObj.listen_port = listen_port.text
                else:
                    ssl = server.find('domain_config:ssl', cns)
                    if ssl is not None:
                        listen_port = ssl.find('domain_config:listen-port', cns)
                        if listen_port is not None:
                            print "listen_port : "+listen_port.text
                            serverObj.listen_port = listen_port.text
                server_cluster = server.find('domain_config:cluster', cns)
                if server_cluster is not None:
                     print "server_cluster : "+server_cluster.text
                     serverObj.server_cluster = server_cluster.text
                domain.add_server(serverObj)
        else:
             print "@@@@ No servers available @@@@"

        """
         Identifying the cluster details
        """
        clusters = config_root.findall('domain_config:cluster', cns)
        print " --------------  clusters: --------------"
        if clusters:
            for cluster in clusters:
                clusterObj = domain_cfg.Cluster()
                cluster_name = cluster.find('domain_config:name', cns)
                if cluster_name is not None:
                     print "cluster_name : "+cluster_name.text
                     clusterObj.cluster_name =  cluster_name.text
                domain.add_cluster(clusterObj)
        """
         Identifying the application details
        """
        applications = config_root.findall('domain_config:app-deployment', cns)
        print " --------------  applications: --------------"
        if applications :
            for application in applications:
                applicationObj = domain_cfg.Application()
                app_name = application.find('domain_config:name', cns)
                if app_name is not None:
                    print "app_name : "+app_name.text
                    applicationObj.app_name = app_name.text

                target_servers = application.find('domain_config:target', cns)
                if target_servers is not None:
                    print "target_servers : "+target_servers.text
                    applicationObj.target_servers = target_servers.text

                module_type = application.find('domain_config:module-type', cns)
                if module_type is not None:
                    print "module_type : "+module_type.text
                    applicationObj.module_type = module_type.text

                app_path = application.find('domain_config:source-path', cns)
                if app_path is not None:
                    print "app_path : "+app_path.text
                    applicationObj.app_path =  app_path.text
                domain.add_application(applicationObj)
                print "---------------------------------"

        """
         Identifying the jdbc data source details
        """
        datasources = config_root.findall('domain_config:jdbc-system-resource', cns)
        print " --------------  datasources: --------------"
        if datasources:
            for datasource in datasources:
                datasourceObj = domain_cfg.Datasource()
                datasource_name = datasource.find('domain_config:name', cns)
                if datasource_name is not None:
                    print "datasource_name : "+datasource_name.text
                    datasourceObj.datasource_name = datasource_name.text

                target_server = datasource.find('domain_config:target', cns)
                if target_server is not None:
                    print "target_server : "+target_server.text
                    datasourceObj.target_server = target_server.text

                datasource_location = datasource.find('domain_config:descriptor-file-name', cns)
                if datasource_location is not None:
                    print "datasource_location : "+datasource_location.text
                    datasourceObj.datasource_location = datasource_location.text

                dns = {'jdbc_datasource_config': 'http://xmlns.oracle.com/weblogic/jdbc-data-source'}
                if datasource_location is not None:
                    datasource_location = datasource_location.text.replace('/', '/')
                    datasource_config_location = domain_location+"/config/"+datasource_location
                    datasource_tree = ET.parse(datasource_config_location)
                    datasource_root = datasource_tree.getroot()
                    """
                     Identifying the data source config details
                    """
                    jdbcdriverparams = datasource_root.findall('jdbc_datasource_config:jdbc-driver-params', dns)
                    if jdbcdriverparams is not None:
                         for jdbcdriverparam in jdbcdriverparams:
                             jdbc_url = jdbcdriverparam.find('jdbc_datasource_config:url', dns)
                             if jdbc_url is not None:
                                 print "jdbc_url:"+jdbc_url.text
                                 datasourceObj.jdbc_url = jdbc_url.text
                             driver_name = jdbcdriverparam.find('jdbc_datasource_config:driver-name', dns)
                             if driver_name is not None:
                                 print "driver_name:"+driver_name.text
                                 datasourceObj.driver_name = driver_name.text

                    jdbcdataparams = datasource_root.findall('jdbc_datasource_config:jdbc-data-source-params', dns)
                    if jdbcdataparams is not None:
                         for jdbcdataparam in jdbcdataparams:
                             jndi_name = jdbcdataparam.find('jdbc_datasource_config:jndi-name', dns)
                             if jndi_name is not None:
                                 print "jndi_name:"+jndi_name.text
                                 datasourceObj.jndi_name = jndi_name.text
                domain.add_datasource(datasourceObj)
                print "---------------------------------------"

        """
         Identifying the jms config details
        """
        jmsresources = config_root.findall('domain_config:jms-system-resource', cns)
        print " --------------  jms resources: --------------"
        if jmsresources:
            for jmsresource in jmsresources:
                jmsresourceObj = domain_cfg.Jmsresource()
                jmsresource_name = jmsresource.find('domain_config:name', cns)
                if jmsresource_name is not None:
                    print "jmsresource_name : "+jmsresource_name.text
                    jmsresourceObj.jmsresource_name = jmsresource_name.text

                target_server = jmsresource.find('domain_config:target', cns)
                if target_server is not None:
                    print "target_server : "+target_server.text
                    jmsresourceObj.target_server = target_server.text

                jmssubdeployments = config_root.findall('domain_config:sub-deployment', cns)
                if jmssubdeployments:
                       for jmssubdeployment in jmssubdeployments:
                           subdeploy_name = jmssubdeployment.find('domain_config:name', cns)
                           if subdeploy_name is not None:
                               print "subdeploy_name : "+subdeploy_name.text
                               jmsresourceObj.subdeploy_name = subdeploy_name.text
                           subdeploy_target = jmssubdeployment.find('domain_config:target', cns)
                           if subdeploy_target is not None:
                               print "subdeploy_target : "+subdeploy_target.text
                               jmsresourceObj.subdeploy_target = subdeploy_target.text

                jmsresource_location = jmsresource.find('domain_config:descriptor-file-name', cns)
                if jmsresource_location is not None:
                    print "jmsresource_location : "+jmsresource_location.text
                    jmsresourceObj.jmsresource_location = jmsresource_location.text

                jns = {'jms_resource_config': 'http://xmlns.oracle.com/weblogic/weblogic-jms'}
                if jmsresource_location is not None:
                    jmsresource_location = jmsresource_location.text.replace('/', '/')
                    jmsresource_config_location = domain_location+"/config/"+jmsresource_location
                    jmsresource_tree = ET.parse(jmsresource_config_location)
                    jmsresource_root = jmsresource_tree.getroot()
                    """
                     Identifying the jms queue config details
                    """
                    jmsqueues = jmsresource_root.findall('jms_resource_config:uniform-distributed-queue', jns)
                    if jmsqueues:
                         for jmsqueue in jmsqueues:
                             jmsQueueObj = domain_cfg.Jmsqueue()
                             jmsqueue_name = jmsqueue.get('name')
                             jmsQueueObj.jmsqueue_name = jmsqueue_name
                             jmsqueue_sub_deploy_name = jmsqueue.find('jms_resource_config:sub-deployment-name', jns)
                             if jmsqueue_sub_deploy_name is not None:
                                 print "jmsqueue_sub_deploy_name:"+jmsqueue_sub_deploy_name.text
                                 jmsQueueObj.jmsqueue_sub_deploy_name = jmsqueue_sub_deploy_name.text

                             jmsqueue_jndi_name = jmsqueue.find('jms_resource_config:jndi-name', jns)
                             if jmsqueue_jndi_name is not None:
                                 print "jmsqueue_jndi_name:"+jmsqueue_jndi_name.text
                                 jmsQueueObj.jmsqueue_jndi_name = jmsqueue_jndi_name.text
                             jmsresourceObj.add_jmsqueue(jmsQueueObj)

                    """
                     Identifying the jms coneection factory details
                    """
                    jmstopics = jmsresource_root.findall('jms_resource_config:uniform-distributed-topic', jns)
                    if jmstopics is not None:
                         for jmstopic in jmstopics:
                             jmstopicObj = domain_cfg.Jmstopic()
                             jmstopic_name = jmstopic.get('name')
                             jmstopicObj.jmstopic_name = jmstopic_name

                             jmstopic_jndi_name = jmstopic.find('jms_resource_config:jndi-name', jns)
                             if jmstopic_jndi_name is not None:
                                 print "jmstopic_jndi_name:"+jmstopic_jndi_name.text
                                 jmstopicObj.jmstopic_jndi_name = jmstopic_jndi_name.text
                             jmsresourceObj.add_jmstopic(jmstopicObj)
                domain.add_jmsresource(jmsresourceObj)
                print "---------------------------------------"

        domain_config_list.append(domain)

    def obj_dict(obj):
        return obj.__dict__

    json_string = json.dumps(domain_config_list, default=obj_dict)
#    obj = unpickler.Unpickler().restore(json_string, classes=Domain)
    print json_string

 except Exception as exp:
   print "Weblogic configuration parsing failed.",exp
   traceback.print_tb(exp.__traceback__)


else:
   print "------ root value is None -------"
