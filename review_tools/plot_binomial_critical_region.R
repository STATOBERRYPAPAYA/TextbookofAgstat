x<-0:10
prob<-dbinom(x,10,.5)
stopifnot(abs(sum(prob[x<=1|x>=9])-.021484375)<1e-14)
draw<-function(){
 par(mar=c(6,5,1,1),family='serif',las=1)
 centres<-barplot(prob,names.arg=x,col=ifelse(x<=1|x>=9,'#ac2020','#565656'),
   border='black',ylim=c(0,.27),ylab='P(X = x)',xlab='',space=.25,cex.names=.95)
 mtext('Number of heads, X',side=1,line=2.3)
 legend('topright',legend=c('Rejection: X = 0, 1, 9 or 10','Do not reject: X = 2 to 8'),
        fill=c('#ac2020','#565656'),bty='n',cex=.78)
 mtext('Under H0: X follows Binomial(10, 0.5)',side=1,line=4,cex=.85)
}
svg('images/hypotest/binomial-critical-region.svg',width=8,height=5.2,bg='white');draw();dev.off()
png('review_tools/binomial-critical-region-preview.png',width=1440,height=936,res=180,bg='white');draw();dev.off()
