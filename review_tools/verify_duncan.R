options(digits=10)
d<-read.csv("csv/duncan.csv",check.names=FALSE)
dif<-data.frame()
for(i in seq_len(nrow(d))){
  df<-as.numeric(d[i,1]);if(is.na(df)||df<2)next
  pp<-2:20
  q<-cummax(qtukey(.95^(pp-1),pp,df))
  for(j in 2:ncol(d)){
    p<-as.numeric(names(d)[j]);v<-as.numeric(d[i,j])
    if(is.finite(v)&&is.finite(q[p-1])&&abs(v-q[p-1])>.006)
      dif<-rbind(dif,data.frame(df,p,printed=v,computed=q[p-1]))
  }
}
write.csv(dif,"review_tools/duncan_comparison.csv",row.names=FALSE)
print(dif)
