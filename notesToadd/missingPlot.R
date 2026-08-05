## MISSING PLOT ANALYSIS  
In agricultural field experiments the experimenter is often encountered with 
the situation that the observations of a particular treatment/ plot may be lost or may be affected by some external factors so that it would not be possible to analyse these observations by including it with the normal values. The observation on a treatment may get lost by various reasons like, attack of cattle or birds, manure may be dumped on the side, disease infestation and so on. The data recorded from plots so affected will be omitted and then the analysis is carried out – called as missing plot analysis.  

The Analysis of such data may be done by different methods. (i) the most 
commonly used method currently adopted is  known as ‘method of analysis of non 
orthogonal data’ which is highly computer based (ii) Method of substitution by Yates based on minimization of the error sum of squares and (iii) Analysis of the data with missing values by the technique of Analysis of Covariance by Bartlett’s.  

**Covariance Method by Bartlett's**  
Assume an imaginary covariate X taking values zero for every plot except the 
missing plot for which it will take the value 1 (or –1) . Now the value of the main variate, Y = 0 for the missing plot, and the actual values for the remaining plots. The data will be analysed as per the ANCOVA technique of the respective design used.  
In missing plot analysis the degrees of freedom for error and total will be 
based on the existing number of observations only. By this method also the degrees of freedom of adjusted error sum of squares will be less by one (when there is one missing value). 

**Method of Substitution**  
$(i)$ In this method we will calculate with the aid of a formula an estimate of the missing value. The formula will vary from design to design and actually it will not supply the exact missing value.  But the procedure permits the researcher to complete the analysis without resorting to more complex procedures.  
$(ii)$ Insert the estimated value in the missing position and workout the estimates of treatment means and mean error sum of squares.  
$(iii)$ Some additional adjustments to treatment sum of squares are needed. In pair comparison also some changes are made.  
$(iv)$ An iterative procedure is adopted when more than one observation is missing.  

### Randomised Block Design with a single missing value  
$(i)$ The missing value in RBD is estimated as 
$$x=\frac{rB+vT-G}{(r-1)(v-1)}$$
where,  
x = estimate of the missing data  
v = number of treatments  
r = number of replications  
B = Total of the observed values of the replication that contain the missing data  
T = Total of the observed values of the treatment that contain the missing data  
G = Grand total of all existing observations.  

$(ii)$ This estimate of the missing value is placed in its position and the analysis is carried out based on the procedure of RBD. Subtract one degree of freedom from the total and error degrees of freedom.  

This method provides a proper estimate of the error variance per plot but there 
is an inflation in treatment sum of squares; (the treatment sum of squares is positively biased). If the treatments turn out to be not significant we can ignore the bias and the results are accepted. But if the treatments turns out to be just significant it may be due to this bias. In that case an actual treatment sum of squares is obtained by a suitable formula. 

$(iii)$ Estimate of Bias in the case of RBD
$$Bias=\frac{(B+vT-G)^2}{v(v-1)(r-1)^2}$$
This bias is subtracted from the treatment sum of squares.  Now test this actual 
treatment mean square against the Mean Square for error:  and make the conclusion about the significance of treatments.  
$(iv)$ Pair comparison  
$(a)$ For comparing two treatment means in which one of them contain a missing observation 
$$C.D. = t_{\alpha}\sqrt{MSE(\frac{2}{r}+\frac{v}{r(r-1)(v-1)})}$$  
$(b)$  For comparing other pairs of  treatment means: (in which none of 
them contain any missing observation)   
$$C.D. = t_{\alpha}\sqrt{2MSE/r}$$ 
where, $t_{\alpha}$ denote the t value (r-1)(v-1)-1 degrees of freedom.  

$(v)$ If there are more than one missing value the estimates of the missing 
values are obtained by an  iteration procedure. 

### Latin Square Design with a single missing value 
The same procedure as in RBD is used here also.  

$(i)$ The missing value in LSD is obtained as
$$x=\frac{v(R+C+T)-2G}{(v-1)(v-2)}$$
where,  
x = estimate of the missing data  
v = number of treatments/rows/blocks/columns    
R = Total of the observed values of the row that contain the missing data   
C = Total of the observed values of the column that contain the missing data  
T = Total of the observed values of the treatment that contain the missing data  
G = Grand total of all existing observations.  

$(ii)$ Carry out the analysis similar to the above method  after substitution. The estimate of Bias in this case is 
$$Bias=\frac{[(v-1)T+R+C-G]^2}{[(v-1)(v-2)]^2}$$

$(iii)$ For pairwise comparison involving a treatment with a missing observation (comparing two treatment means in which one of them contains a missing observation):
$$C.D. = t_{\alpha}\sqrt{MSE\left(\frac{2}{v}+\frac{1}{(v-1)(v-2)}\right)}$$