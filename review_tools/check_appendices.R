options(warn=1)
invisible(Sys.setlocale('LC_ALL','English_United States.utf8'))
bad<-list(); checked<-0L
compare<-function(file, fun) {
 d<-read.csv(file,check.names=FALSE,colClasses='character',fileEncoding='UTF-8')
 for(i in seq_len(nrow(d))) for(j in 2:ncol(d)) {
   a<-suppressWarnings(as.numeric(d[i,j])); if(is.na(a))next
   row<-suppressWarnings(as.numeric(gsub('∞','Inf',d[i,1],fixed=TRUE)))
   col<-suppressWarnings(as.numeric(gsub('∞','Inf',names(d)[j],fixed=TRUE)))
   if(is.na(row)||is.na(col))next
   expected<-suppressWarnings(fun(row,col)); if(!is.finite(expected))next
   decimals<-if(grepl('.',d[i,j],fixed=TRUE))nchar(sub('.*\\.','',d[i,j])) else 0
   tol<-.51*10^(-decimals)
   checked<<-checked+1L
   if(abs(a-expected)>tol) bad[[length(bad)+1L]]<<-data.frame(file=file,row=d[i,1],column=names(d)[j],printed=a,calculated=expected)
 }
}
compare('csv/ztable.csv',function(r,c)pnorm(r+c))
compare('csv/ttable.csv',function(r,c)qt(c,r))
compare('csv/ftable_05.csv',function(r,c){if(is.infinite(r)&&is.infinite(c))1 else if(is.infinite(r))qchisq(.95,c)/c else if(is.infinite(c))r/qchisq(.05,r) else qf(.95,c,r)})
capture.output({cat('Checked',checked,'normal, t, and F table cells against R distributions.\n');if(length(bad))print(do.call(rbind,bad),row.names=FALSE)else cat('All within the rounding precision shown.\n'); cat('Duncan table: not judged by raw qtukey values, which differ from the traditional monotone critical-range convention. Source comparison required.\n')},file='review_tools/appendix_check_results.txt')
cat('Appendix checks saved\n')
