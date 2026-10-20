options(digits=12)
results<-list()
check<-function(label,value,expected,tol=1e-7){
 stopifnot(all(is.finite(value)),max(abs(value-expected))<=tol)
 results[[length(results)+1]]<<-data.frame(check=label,computed=paste(value,collapse='; '),expected=paste(expected,collapse='; '))
}
check('Graph median in original example',150+(25-9)/17*10,159.4117647)
check('New grouped percentile and decile',c(20+(15-12)/6*10,10+(12-4)/8*10),c(25,20))
check('Combined groups mean/variance/SD',c((3*4+2*6)/5,(2*1^2+1*2^2+3*(4-4.8)^2+2*(6-4.8)^2)/4,sqrt(2.7)),c(4.8,2.7,1.6431676725))
check('Six-card red/black probability',choose(26,3)^2/choose(52,6),.3320477123)
# Exclude the displayed total row from the 12-observation regression data.
d<-read.csv('csv/Book12.csv')[1:12,];x<-d[[2]];y<-d[[3]]
check('Reverse regression coefficients',coef(lm(x~y)),c(6.41280531,.03047139),1e-8)
check('First fitted yield and residual',c(predict(lm(y~x))[1],residuals(lm(y~x))[1]),c(267.77349,-52.77349),1e-5)
check('ANOVA one-percent critical value',qf(.99,5,18),4.247882,1e-6)
check('Graph exercises angles/densities/median/fences',c(c(40,35,25)*360/100,8/10,12/20,10+(5-2)/5*10,12-1.5*8,20+1.5*8),c(144,126,90,.8,.6,16,0,32))
check('Basic exercises Sturges/frequencies/boundaries',c(1+3.322*log10(100),sum(c(4,7,6,3)),2/5,(20+24)/2,24.5-19.5),c(7.644,20,.4,22,5))
check('Official-statistics exercises',c(10000*8.5/25,10*3,5.2-.2,6*sqrt(2)),c(3400,30,5,8.4852813742))
d<-read.csv('review_tools/uniformity_verified.csv')
check('Free-intercept Smith fit versus anchored fit',c(-coef(lm(log(Vx)~log(x),d))[2],-coef(lm(log(Vx/Vx[1])~0+log(x),d))[1]),c(.3468119,.360686601),1e-7)
# Grouping for the Latin-square worked example.
m<-c(D=42,A=37.6,B=34.2,C=28.4,E=23.6)
letters<-c(D='a',A='ab',B='b',C='c',E='c')
for(i in 1:4)for(j in (i+1):5){
 shared<-length(intersect(strsplit(letters[i],'')[[1]],strsplit(letters[j],'')[[1]]))>0
 stopifnot(shared==(abs(m[i]-m[j])<5.07))
}
write.csv(do.call(rbind,results),'review_tools/external_review_additions_verified.csv',row.names=FALSE)
cat(length(results),'external-review numeric checks and all ten grouping comparisons passed.\n')
