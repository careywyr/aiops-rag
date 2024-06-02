## 一些记录

doctype.xml里面的id没啥用，但内容在nodetree里面可以找到doctype

每个文件夹下的子文件夹并不代表他们是同级的，实际上还是要以nodetree.xml里面为准

``` shell
docker run -d --name neo4j \  
	-p 7474:7474 -p 7687:7687 \  
	-v /Users/carey/Documents/docker_data/neo4j/data:/data \  
	-v /Users/carey/Documents/docker_data/neo4j/logs:/logs \  
	-v /Users/carey/Documents/docker_data/neo4j/conf:/var/lib/neo4j/conf   
	-v /Users/carey/Documents/docker_data/neo4j/import:/var/lib/neo4j/import \  
	--env NEO4J_AUTH=neo4j/password \  
	neo4j:5.20.0-community-ubi9 
	
docker run -d -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "network.host=0.0.0.0" \
  -e "xpack.security.enabled=false" \
  -v /Users/carey/Documents/docker_data/es/data:/usr/share/elasticsearch/data \
  --name elasticsearch elasticsearch:8.13.0 

```


## 向量化的想法或者说数据存储的想法
遍历nodetree，找到那种没有子节点的html，把这个html的内容转换成md进行向量化，文本内容以及向量存储到es，并且要附赠上目录树，作为此文档的关键词。