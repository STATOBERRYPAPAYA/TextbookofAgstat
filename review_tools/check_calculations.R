options(digits=10)
capture.output({
cat('TRANSFORMATIONS: calculations from printed raw observations\n')
weed <- matrix(c(169,132,180,105,210,172,158,125,160,94,103,65,100,120,98,74,42,40,84,28,368,300,610,200),6,4,byrow=TRUE)
larva <- matrix(c(9,12,0,1,4,8,5,1,6,15,6,2,9,6,4,5,27,17,10,10,35,28,2,15,1,0,0,0),7,4,byrow=TRUE)
mortality <- matrix(c(0,0,3,2,12,15,18,17,33,30,35,34,52,54,58,55,86,78,80,79,88,79,100,100),6,4,byrow=TRUE)
rcbd <- function(m) {
  d<-data.frame(y=as.vector(t(m)),trt=factor(rep(seq_len(nrow(m)),each=ncol(m))),block=factor(rep(seq_len(ncol(m)),nrow(m))))
  fit<-aov(y~trt+block,d); print(anova(fit)); print(m); print(rowSums(m)); print(colSums(m)); print(rowMeans(m));
  cat('CF',sum(m)^2/length(m),'sum squares',sum(m^2),'LSD',qt(.975,df.residual(fit))*sqrt(2*deviance(fit)/df.residual(fit)/ncol(m)),'\n')
  invisible(fit)
}
cat('\nLOG WEED\n'); rcbd(log10(weed)); print(10^rowMeans(log10(weed)))
cat('\nSQRT LARVA\n'); rcbd(sqrt(larva+1)); print(rowMeans(sqrt(larva+1))^2-1)
cat('\nANGULAR MORTALITY: endpoint p = 1/(4n), 1-1/(4n), n=100\n')
p<-mortality/100; p[p==0]<-1/400; p[p==1]<-1-1/400
ang<-asin(sqrt(p))*180/pi; print(ang); print(rowSums(ang)); print(rowMeans(ang));
d<-data.frame(y=as.vector(t(ang)),trt=factor(rep(1:6,each=4)))
fit<-aov(y~trt,d); print(anova(fit)); cat('LSD',qt(.975,18)*sqrt(2*deviance(fit)/18/4),'\n'); print(100*sin(rowMeans(ang)*pi/180)^2)
cat('\nMISSING PLOT RCBD: full precision and exact model fit\n')
m<-matrix(c(.679,.852,.513,.507,.952,1.002,NA,.621,.899,.919,.718,.679,.986,.949,.845,.780,.911,.922,.668,.746),5,4,byrow=TRUE)
G<-sum(m,na.rm=TRUE); B<-sum(m[,3],na.rm=TRUE); T<-sum(m[2,],na.rm=TRUE)
x<-(4*B+5*T-G)/(3*4); cat('Observed G,B,T',G,B,T,'Estimated x',x,'\n')
m[2,3]<-x; print(m); print(rowSums(m)); print(colSums(m)); print(rowMeans(m)); cat('CF',sum(m)^2/20,'sum squares',sum(m^2),'\n'); rcbd(m)
cat('Bias',(B+5*T-G)^2/(5*4*3^2),'\n')
dat<-data.frame(y=as.vector(t(m)),trt=factor(rep(1:5,each=4)),block=factor(rep(1:4,5)))
dat<-dat[-7,]; fit<-lm(y~block+trt,dat); print(anova(fit)); cat('SSE',deviance(fit),'MSE',deviance(fit)/df.residual(fit),'df',df.residual(fit),'\n')
cat('\nSELECTED TEST CRITICAL VALUES\n'); print(qf(c(.95,.975),10,7)); print(qchisq(c(.025,.975),14)); print(qf(.95,6,18)); print(qf(.95,3,18)); print(qt(.975,18)); print(qt(.975,15))
cat('\nSELECTED EXERCISE RESULTS\n'); print(t.test(c(5,2,8,-1,3,0,-2,1,5,0,4,6),alternative='greater')); print(sum((c(103,143,98,42,8,6)-c(106,141,93,41,14,5))^2/c(106,141,93,41,14,5)))
}, file='review_tools/calculation_results.txt')
cat('Independent calculations saved to review_tools/calculation_results.txt\n')
