options(digits=12)
data(rice,package="agricolae")
A<-as.matrix(rice[1:15,1:10])
stopifnot(sum(A)==122777,sum(A^2)==101325715)
shapes<-read.csv("csv/Book20.csv",check.names=FALSE)
out<-do.call(rbind,lapply(seq_len(nrow(shapes)),function(i) {
  width<-shapes[i,3];height<-shapes[i,4];x<-width*height
  totals<-c()
  for(row in seq(1,nrow(A),height)) for(col in seq(1,ncol(A),width))
    totals<-c(totals,sum(A[row:(row+height-1),col:(col+width-1)]))
  ss<-sum(totals^2)/x-sum(A)^2/length(A)
  v<-ss/(length(A)-x)
  stopifnot(abs(v-var(totals/x))<1e-7)
  data.frame(x,width,height,w=length(totals),SS=ss,Vx=v,CV=100*sqrt(v)/mean(A),sampleVarianceOfMeans=var(totals/x),fieldScaledVariation=ss/(length(A)-1))
}))
write.csv(out,"review_tools/uniformity_verified.csv",row.names=FALSE)
capture.output({
  print(out)
  X<-log(out$x);Y<-log(out$Vx/out$Vx[1])
  b<- -sum(X*Y)/sum(X^2)
  print(c(b=b,adjusted=.403+(b-.35)*(.443-.403)/(.4-.35)))
  print(c(SSvertical=sum(colSums(A)^2)/15-sum(A)^2/150,
          SShorizontal=sum(rowSums(A)^2)/10-sum(A)^2/150))
  print(c(horizontalCircular=sum(A*cbind(A[,-1],A[,1])),
          verticalCircular=sum(A*rbind(A[-1,],A[1,]))))
  print(agricolae::index.smith(as.data.frame(A),PLOT=FALSE)$uniformity)
},file="review_tools/uniformity_verified.txt")
write.csv(A,"review_tools/uniformity_raw.csv",row.names=FALSE)
