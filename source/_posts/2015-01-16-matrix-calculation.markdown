---
layout: post
title: "Matrix Calculation"
date: 2015-01-16 21:34:18 +0800
comments: true
categories: 
---

## Basic notations:


In the following descriptions, $x \in R^n $, $b \in R^n$ and $X \in
R^{n \times n}$, $A \in R^{n \times n}$ and $f (x) \in R, f (X) \in
R^{}$. To start, we first standardize the following basic notations:

* $$\frac{\partial (b^T x)}{\partial x} = \frac{\partial (x^T
  b)}{\partial x} = \nabla_x tr (b^{^T} x) = \nabla_x tr (b^{^{}} x^T)=b$$
  
* $$\frac{\partial (tr (A^T X))}{\partial X} = \frac{\partial (tr (^{}
  X^T A))}{\partial X} = \nabla_X tr (A^T X) = \nabla_X tr (A^{} X^T) = A$$


## Another way to illustrate the basic notations:

* $$d [tr (f (x)] = tr(d(f(x)) = tr[(\nabla_x f (x))^T d x]$$

* $$d [tr (f (X)] = tr(d(f(X)) = tr[(\nabla_X f (X))^T d X]$$





***


## Chain rule:



$$d [tr (g (x) h (x)) = tr [d (g (x) \cdot h (x))]$$ 

$$ tr [d (g (x) \cdot h (x))] = tr[(\nabla_x g (x))^T d x \cdot h (x) + g (x) \cdot (\nabla_x h (x))^T d x]$$

$$d [tr (g (x) h (x)) =  tr [(h (x) (\nabla_x g (x))^T + g (x) \cdot (\nabla_x h (x))^T) d x]$$


 An illustration of chain rule:
 
  $$ d (x^T A x) = tr [d (x^T A x)] = tr [d (x^T) A x + x^T A d x]$$ 
  
  $$ d (x^T A x) = tr [(d
   x)^T A x + x^T A d x] = tr [((A x)^T + x^T A) d x] $$

As such, 

$$\frac{\partial (x^T A x)}{\partial x} = ((A x)^T + x^T A)^T = (A + A^T) x$$



and 

$$d (tr [X A X]) = tr [(A X + X A) d X]$$ 

$$\frac{\partial (tr [X
A X])}{\partial x} = (A X + X A)^T = X^T A^T + A^T X^T$$



*** 



## Derivative of determinant

It holds that $A A^{\ast} = | A | I$ 
where $A^{ \ast }$ 
is the Adjugate matrix of $A$, hence, 

$$|A| = tr(A A^{\ast})$$

and 

$$\frac{\partial (|A|)}{\partial A} = \nabla_A [tr (A A^{\ast})] = (A^{\ast})^T$$

If $A$ is a non-singular matrix, the following equations hold:

$$A^{\ast} = |A| A^{- 1}$$

$$\frac{\partial(|A|)}{\partial A} = |A| (A^{- 1})^T$$ 

If A is also symmetric, 

$$A^{- 1} = {diag} (A^{-1})$$

It then immediately follows that: 

$$\frac{\partial (\ln | A |)}{\partial A} = (A^{-
1})^T$$



***



## Three commonly used tricks about matrix calculation:

* $A \in S^n$, $A = U \Sigma U^T$ where $U$ is an orthogonal matrix and $A = A^{1/2} A^{1/2}$ where $A^{1/2} = U \Sigma^{1/2} U^T$;
  
* If $\| x \| = 1$, then $(I + \lambda x x^T)^{- 1} = I -
  \frac{\lambda}{1 + \lambda} x x^T$;
  
* $A \in S^{n}$, $\ln |I + A| = \sum_{i = 1}^n \ln (1 +
  \lambda_i)$ where $\lambda_1, \lambda_2, \ldots, \lambda_n$ are the eigenvalues of $A$ and $\lambda_i > - 1$. 

