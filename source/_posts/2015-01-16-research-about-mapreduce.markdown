---
layout: post
title: "Research about MapReduce"
date: 2015-01-16 20:06:35 +0800
comments: true
categories: 
---

In this blog, I mainly talk about three important research issues for MapReduce framework which are:

* **Job scheduling for minimizing the total response time**
* **Data locality issue**
* **Speculative Execution**
 
For each issue I will make two categories which are theoretical analysis based optimization and heuristic based algorithm  design. Hope you can get something useful from this summary.


***

## Some new papers related to MapReduce scheduling and task cloning
* [The Power of Choice in Data-Aware Cluster Scheduling](https://www.eecs.berkeley.edu/~apanda/papers/kmn.pdf) This paper acutally studies two problems which are speculative execution and data locality. 

## Job Scheduling

### Theoretical Analysis based:

* [B. Moseley, A. Dasgupta, R. Kumar, and T. Sarlos, “On scheduling in map-reduce and flow-shops,” in SPAA 2011.](http://dl.acm.org/citation.cfm?id=1989493.1989540) This paper seeks to minimize the _flowtime_ of jobs which is motivated from the two-stage flow shop problem. The tasks to machine mapping is unknown and needs to be determined such that the total _flowtime_ is minimized. It gives the offline and online algorithm in both homogeneous and heterogenous environment. The analysis here is nontrivial and gives us a flavor how traditional SRPT algorithm can apply to the scheduling in MapReduce System. 




* [Hyunseok Chang, Murali Kodialam, Ramana Rao Kompella, T. V. Lakshman, Myungjin Lee, Sarit Mukherjee, "Scheduling in MapReduce-like Systems for Fast completion time," in Infocom 2011.](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=5935152&tag=1) This paper seeks to optimize the total completion time of job running in the Mapreduce system. It decides the scheduling order of tasks on each processor. Moreover, this paper doesn't consider the dependency between map task and reduce tasks. A linear program is formulated to relax the original problem. It then outlines a combinatorial approach to solve the LP problem.

* [F. Chen, M. Kodialam, and T. Lakshman, “Joint scheduling of processing and shuffle phases in MapReduce systems,” in Infocom 2012.](http://www.cse.psu.edu/~fachen/pubs/infocom12mr.pdf) 
Actually this paper is the follow-up work of the above paper. To be more practical, it considers the dependency between map and reduce tasks. Moreover, it jointly optimizes the job completion time by imposing the shuffle phase constraint. 

* [Jian Tan, Xiaoqiao Meng, Li Zhang, “Delay Tails in MapReduce Scheduling,” in SIGMETRICS 2012.](http://dl.acm.org/citation.cfm?id=2254761) This paper focuses on the the starvation issue of small jobs under fair scheduler in MapReduce. The root reason of this problem is caused by launching the reduce tasks so early. To efficiently solve this issue and improve the job response performance, it presents a couple scheduler which assign the reduce tasks based on the progress of the map phase. The theoretical analysis here is very complicated. 

* [Yousi Zheng, Ness Shroff, Prasun Sinha, “A New Analytical Technique for Designing Provably Efficient MapReduce Schedulers,” in Infocom 2013](http://newslab.ece.ohio-state.edu/research/resources/Analysis.pdf). This paper is the first work to write down the formulation of mapreduce job scheduling including both map and reduce phases. There is no distinguish between map and reduce slots here. It uses adopts the knowledge in probability to prove that any work-conserving scheduler can achieves a constant efficiency ratio (not competitive ratio). Moreover, this paper presents the ASRPT algorithm which is inspired from the famous SRPT (Shortest remaining time first) algorithm and bound the competitive ratio to be 2.

* [M. Lin, L. Zhang, A. Wierman and J. Tan, "Joint optimization of overlapping phases in MapReduce," in IFIP 2013.](http://users.cms.caltech.edu/~adamw/papers/preprint_mapreduce.pdf). This is the first work to consider the overlapping of map phase and shuffle phase so far. A nice formulation is also written down here. Hover, even the offline case with batch arrival is shown to be NP-Complete. It then presents the MaxSRPT ans SpiltSRPT algorithm which are complementary to solve schedule the jobs.




### Heuristic based:

I haven't read any papers which present heuristic-based algorithm to optimize the job completion time in MapReduce system. 

***

## Data locality
 
### Theoretical Analysis based: 

* [Qiaomin Xie, Yi Lu, “Degree-guided map-reduce task assignment with data locality constraint,” in ISIT 2012.](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=6284711&tag=1) This paper presents the peeling algorithm and adopts the mean-field equations to analyze the evolution (I cannot understand it well). However, it makes an impractical assumption which is that all the tasks with data locality on the machine can be finished in a time slot with probability _p_ while the tasks without data locality can only be finished with probability _q_ and **p > q**. Also the theoretical here is very complex. 

* [W. Wang, K. Zhu, L. Ying, J. Tan, L. Zhang, "Map Task Scheduling in MapReduce with Data Locality: Throughput and Heavy-Traffic Optimality," in Infocom 2013](http://inlab.lab.asu.edu/Publications/WanZhuYin_13.pdf). This paper makes the same assumption as the above paper presented in ISIT 2012. Its task scheduling algorithm includes two aspects which are `Routing` and `Scheduling`. The purpose of routing is to keep load balancing for all the machines. Also scheduling process makes a very simple decision based on the length of queues. It adopts the Lyapunov function to prove the stability of the algorithm. The analysis here is also nontrivial. 

* [J. Tan, X. Meng, L. Zhang, "Improving ReduceTask Data Locality for Sequential MapReduce Jobs," in Infocom 2013.](https://www.google.com.hk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&ved=0CDIQFjAB&url=http%3A%2F%2Fresearcher.watson.ibm.com%2Fresearcher%2Ffiles%2Fus-tanji%2FreducePlace2013.pdf&ei=Uh4rUq5mrMGJB-j5gNAJ&usg=AFQjCNEGqVhyg8P3Vj5uOxx7QUrrei4ZQg) This is the first paper to analyze the data locality issue for reduce tasks with theoretical analysis. Actually, the model here is quite simple, the objective is only to minimize the data transfer cost in shuffle phase with proper reduce task placement. The data transfer cost gives a very good angle for analyzing data locality issue.  


### Heuristic based:

* [Michael Isard, Vijayan Prabhakaran, Jon Currey, Udi Wieder, Kunal Talwar and Andrew Goldberg, "Quincy: Fair Scheduling for Distributed Computing Clusters," in SOSP 2009.](http://www.sigops.org/sosp/sosp09/papers/isard-sosp09.pdf) This is the first paper to address the data locality issue and fairness problem in MapReduce-like systems. It encodes the scheduling as a flow network. In this network, the edge weights encode the demands of data locality and fairness. This is a very novel and beautiful work. 

* [Matei Zaharia, Dhruba Borthakur, Joydeep Sen Sarma, Khaled Elmeleegy, Sunnyvale, Scott Shenker, Ion Stoica, "Delay scheduling: a simple technique for achieving locality and fairness in cluster scheduling," in EuroSys 2010.](http://dl.acm.org/citation.cfm?id=1755940) This paper is very famous among all the papers which address the data locality issue. It presents the delay scheduling algorithm which delay the job at the head of the queue a little bit if data locality is not achieved with the available slot. As described next, this algorithm has a obvious drawback: there exists a probability that some slots wont'e be launching any tasks and keeps idle all the way. This phenomenon waste the resource in the cluster and needs to be improved. 

* [J. Tan, X. Meng, L. Zhang, "Coupling Task Progress for MapReduce Resource-Aware Scheduling", in Infocom 2013](http://researcher.watson.ibm.com/researcher/files/us-tanji/coupling2013.pdf). This paper mainly includes 3 pieces of work and for each work a heuristic-based algorithm I is proposed: 
1) Compute the mismatch between the map and reduce progress. The job gets the maximum mismatch value has the highest priority to assign a reduce task. 
 2) Waiting scheduling for reduce task. The main idea behind this algorithm is to assign a reduce task to an available slot who is close to the 'centrality' of the already generated intermediate date produced by the map phase. 
 3) Random peaking algorithm to assign the map task. This algorithm is motivated from the famous 'delay scheduling' algorithm may cause a bad resource utilization level. 
Actually, the heuristic algorithm for assigning map tasks is very complex to implement and doesn't make a clear intuition.  However, the bad resource utilization for 'Delay Scheduling' is a very good observation.

***

## Speculative execution


### Heuristic based:

* [J. Dean and S. Ghemawat, “MapReduce: Simplified Data Processing on Large Clusters”, in USENIX OSDI, 2004.](http://research.google.com/archive/mapreduce-osdi04.pdf)
 Actually, this paper is the technical report to the MapReduce system design of Google. It talks about the back up strategy with a short paragraph. The strategy is that  when a MapReduce operation is close to complete, it will randomly choose some remaining tasks and launch the duplicates of them on alternative machines. It concludes that this speculative execution scheme can decrease the job execution time by 44%.

* [M. Zaharia, A. Konwinski, A. D. Joseph, R. Katz, and I. Stoica, “Improving mapreduce performance in heterogeneous environments,” in OSDI 2008.](http://bnrg.eecs.berkeley.edu/~randy/Courses/CS268.F08/papers/42_osdi_08.pdf) In this paper, a new strategy named LATE is presented. LATE monitors the progress rate of the tasks and estimates their remaining time. Tasks with their progress rate below _slowTaskTherehold_ are chosen as backup candidates and the one with the longest remaining time is given the highest priority when the number of backups in the cluster does not exceed _speculativeCap_.

* [G. Ananthanarayctions of Computer Networks 2013.](http://www.computer.org/csdl/trans/tc/preprint/06419699-abs.html) This paper proposes a Smart Speculative Execution algorithm. The main contributions it makes are twofold: i) Use exponentially weighted moving average to predict process speed and compute a task’s remaining time; ii) Determine which task to backup based on the load of a cluster using a cost-benefit model.

 
```
In our following research, we can consider to optimize 
the job scheduling in a heterogeneous environment where
the machines are not identical.
```
