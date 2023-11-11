# NSGA2--FSDRSA
An evolutionary algorithm for solving disassembly line balancing problems
Tree release version (based on class) and some improvements (initialization method)

Use class-based tree structure storage method initialization method

**************************************************************************************************************************************************************************

Dear experts and engineers,

If our work has been helpful to you, we kindly ask that when you achieve outstanding research results, you cite the following paper in your references. Our entire team, including myself and 22 other members, would be very grateful.

Paper: "Dual-Side Disassembly Line Balancing Problem with Job Rest Time: Constraint Programming Model and Improved NSGA II Algorithm"

We will periodically update relevant materials and our thoughts. However, because our team is also undertaking some other research tasks (and may consider further sharing of dynamic multi-objective optimization, deep reinforcement learning, and deep learning technology applications in industry in the future), often with project engineering requirements, updates may be delayed. But with each update, we will not only upload code but also add some of our thoughts. Additionally, we have related research based on the NSGA2--FSDRSA algorithm that is currently in the preparation for publication stage, and after publication, we will gradually upload relevant materials. We also welcome experts to review them.

Once again, thank you for recognizing our work.

Sincerely,
The entire team

**************************************************************************************************************************************************************************

Motivation and approach: Recently, while having a meal, we discussed the effectiveness of our method. Through these discussions, our team believes that the reason our method is effective is because we have efficiently integrated the concept of "avoiding duplicate searches" with the characteristics of the problem we are solving. This conclusion came from a conversation between my friend Matthew and a senior professor. In their discussion, they mentioned the Monte Carlo search algorithm in AlphaGo, and he realized that the key idea used in the algorithm is to avoid duplicate searches. Then he thought about immune algorithms, ant colony algorithms, etc., and believed that they all incorporate mathematical formulas (such as distance calculation and search frequency calculation) to avoid duplicate searches during the search process. This inspired us, and we concluded that from an algorithmic perspective, our method does not deviate from this idea. Recently, in the actual engineering application process, our team also evaluated our method. We believe that the success of our method is because we have effectively integrated the above concept with the disassembly line balancing problem. In fact, many algorithms inadvertently incorporate the idea of avoiding duplicate searches. I personally believe that methods with this idea can achieve the same effect as our method, but the premise of achieving the effect of our method is to effectively integrate the concept of "avoiding duplicate searches" into the problem to be solved. For example, in ant colony algorithms, there is the concept of pheromones, and effectively integrating this concept with the characteristics of the disassembly line balancing problem is crucial.
