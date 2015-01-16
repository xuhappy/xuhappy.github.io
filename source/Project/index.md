{% capture root_url %}{{ site.root | strip_slash }}{% endcapture %} {% include head.html %}
{% include header.html %}
{{ content | expand_urls: root_url }}
{% include footer.html %}
{% include after_footer.html %}


# Resource management and job scheduling in Cloud Computing #

 `` Cloud computing has become a important comuting paradigm and the critical issue is the service quality. In this way, we aim to design smart algorithms in cloud computing environment so as to improve the job performance. At present, we mainly focus on two metrics of job which are completion time and resource consumption. To achieve this two goals, we consider two factors to optimize including speculative execution and data locality. ``


### 1. Speculative Execution for a single job in a MapReduce-like cluster

Parallel processing plays an important role for large-scale data analytics. It breaks a job into many small tasks which run parallel on multiple machines such as MapReduce framework. One fundamental challenge faced to such parallel processing is the straggling tasks as they can delay the completion of a job seriously.

In this project, we focus on the speculative execution issue which is used to deal with the straggling problem in the literature. We present a theoretical framework for the optimization of a single job which differs a lot from the previous heuristics-based work. More precisely, we propose two schemes when the number of parallel tasks the job consists of is smaller than cluster size. In the first scheme, no monitoring is needed and we can provide the job deadline guarantee with a high probability while achieve the optimal resource consumption level. The second scheme needs to monitor the task progress and makes the optimal number of duplicates when the straggling problem happens. On the other hand, when the number of tasks in a job is larger than the cluster size, we propose an Enhanced Speculative Execution (ESE) algorithm to make the optimal decision whenever a machine is available for a new scheduling. The simulation results show the ESE algorithm can reduce the job flowtime by 50% while consume fewer resources comparing to the strategy without backup.

![scheduling model](model_1.jpg =600x360)


**Publications**

* Huanle Xu, Wing Cheong Lau, "Resource Optimization for Speculative Execution in a MapReduce Cluster," in the Procs. of IEEE ICNP (PhD Forum), Oct 2013.
 
* Huanle Xu, Wing Cheong Lau, "Speculative execution for a single job  in a MapReduce-like system," in IEEE Cloud, June  2014.
