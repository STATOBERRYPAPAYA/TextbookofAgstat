f<-c(3,6,17,13,8,3)
edges<-seq(130,190,10)
mid<-seq(135,185,10)
stopifnot(sum(f)==50)
draw<-function(kind) {
 par(mar=c(4.5,4.5,1,1),family='serif',las=1)
 if(kind=='lesser')plot(edges,c(0,cumsum(f)),type='o',pch=19,col='#28776b',lwd=2,
   xlab='Plant height (cm)',ylab='Less than cumulative frequency',ylim=c(0,50),xaxs='i')
 if(kind=='greater')plot(edges,c(50,50-cumsum(f)),type='o',pch=19,col='#28776b',lwd=2,
   xlab='Plant height (cm)',ylab='Greater than cumulative frequency',ylim=c(0,50),xaxs='i')
 if(kind=='polygon')plot(c(125,mid,195),c(0,f,0),type='o',pch=19,col='#1262a3',lwd=2,
   xlab='Plant height (cm)',ylab='Frequency',ylim=c(0,18),xaxs='i')
 if(kind=='histopolygon') {
  plot(NA,xlim=c(125,195),ylim=c(0,18),xlab='Plant height (cm)',ylab='Frequency',xaxs='i',yaxs='i')
  rect(edges[-7],0,edges[-1],f,col='#e7ecee',border='#444444')
  lines(c(125,mid,195),c(0,f,0),type='o',pch=19,col='#1262a3',lwd=2)
 }
}
names<-c(lesser='lesser-ogive-corrected',greater='greater-ogive-corrected',
 polygon='frequency-polygon-corrected',histopolygon='histopolygon-corrected')
for(kind in names(names)){
 svg(paste0('images/',names[kind],'.svg'),width=6.5,height=4.5,bg='white');draw(kind);dev.off()
}
png('review_tools/reviewer-figure-preview.png',width=1400,height=1000,res=160,bg='white')
par(mfrow=c(2,2));for(kind in names(names))draw(kind);dev.off()
cat('Four source-data plots redrawn with the correct cumulative endpoints and polygon closure.\n')
