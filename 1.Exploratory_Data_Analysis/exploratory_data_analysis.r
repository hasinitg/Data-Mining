#**********print summary*******************
w = read.table("C:/HASINI/Purdue/LectureNotes/DataMining/HW1/yelp.dat.txt",header=TRUE,sep=";",quote="\"",comment.char="")
print(summary(w))

#**********print histogram*****************
tip_counts=w[,"tip_count"]
hist(tip_counts,main="Histogram of Tip Counts")

log_of_tip_counts = log(tip_counts)
hist(log_of_tip_counts, main="Histogram of Log of Tip Counts",xlab="log(tip_counts)")

#*******print density plots***************** 
d = density(tip_counts)
plot(d,main="Density of tip_counts",xlab="tip_counts", ylab="density")

f = density(log_of_tip_counts)
plot(f,main="Density of log of tip_counts", xlab="log(tip_counts)", ylab="density")

########check the structure of the data frame
str(w)

###########plot histogram of continuous attribute with maximum range#################
k <- sapply(w,is.factor)
l=which(!k)

cont_attr = w[,l]
cols = colnames(cont_attr)
max_range = 0
max_range_attr = ""
for(col in cols){
  cont_attr_vector = cont_attr[,col]
  r = range(cont_attr_vector)
  d = diff(r)
  if(d>max_range){
    max_range=d
    max_range_attr = col
  }
}
hist(cont_attr[,max_range_attr],main=paste("Histogram of",max_range_attr),xlab=max_range_attr)

##########bar plot of the descrete attribute with maximum number of values##############
m=which(k)
#print(k)

discrete_attr = w[,m]
cols = colnames(discrete_attr)
max_levels = 0
max_levels_attr=""
id_cols = c("business_id","name","address")
for(col in cols){
  if(col %in% id_cols){
    next
  }
  f = factor(w[,col])
  l = nlevels(f)
  print(col)
  print(l)
  if(l>max_levels){
    max_levels = l
    max_levels_attr = col
  }
}
print(max_levels_attr)
#barplot(table(w[,max_levels_attr]),width=10,space=1/10,beside=TRUE,main=paste("Bar plot of ",max_levels_attr," feature."),cex.axis = 0.5,las=2)

############################compute pairwise correlation#############################
lat_long = cor(w[,"latitude"],w[,"longitude"])
print("pairwise correlation of latitude and longitude:")
print(lat_long)

lat_stars = cor(w[,"latitude"],w[,"stars"])
print("pairwise correlation of latitude and stars:")
print(lat_stars)

lat_likes = cor(w[,"latitude"],w[,"likes"])
print("pairwise correlation of latitude and likes:")
print(lat_likes)

long_stars=cor(w[,"longitude"],w[,"stars"])
print("pairwise correlation of longitude and stars:")
print(long_stars)

long_likes=cor(w[,"longitude"],w[,"likes"])
print("pairwise correlation of longitude and likes:")
print(long_likes)

stars_likes=cor(w[,"stars"],w[,"likes"])
print("pairwise correlation of stars and likes:")
print(stars_likes)

#######Scatter plot representing the attributes which has the largest positive correlation###########
plot(w[,"latitude"],w[,"longitude"],main="Scatter plot of latitude and longitude",xlab="latitude",ylab="longitude")

#######Scatter plot representing the attributes which has the largest negative correlation###########
plot(w[,"longitude"],w[,"likes"],main="Scatter plot of longitude and likes",xlab="longitude",ylab="likes")

####################binary features#############################
cat = "Italian"
cat_col = w[,"categories"]
i=1
binary_rest = vector('integer');
for(cell in cat_col){
  if(grepl(cat,cell)){
    binary_rest[i] = 1
  } else {
    binary_rest[i] = 0
  }   
  i=i+1
}
ww = cbind(a=binary_rest,w)
boxplot(stars~a,data=ww,main="Boxplot of binary feature of Italian category vs stars.", xlab="binary feature of Italian category.",ylab="stars")
boxplot(likes~a,data=ww,main="Boxplot of binary feature of Italian category vs likes.", xlab="binary feature of Italian category.",ylab="likes")

cat1 = "Indian"
cat2 = "Chinese"
cat3 = "Fast Food"

i=1
binary_rest = vector('integer');
for(cell in cat_col){
  if(grepl(cat1,cell)){
    binary_rest[i] = 1
  } else {
    binary_rest[i] = 0
  }   
  i=i+1
}
ww = cbind(b=binary_rest,w)
boxplot(stars~b,data=ww,main="Boxplot of binary feature of Indian category vs stars.", xlab="binary feature of Indian category.",ylab="stars")

i=1
binary_rest = vector('integer');
for(cell in cat_col){
  if(grepl(cat2,cell)){
    binary_rest[i] = 1
  } else {
    binary_rest[i] = 0
  }   
  i=i+1
}
ww = cbind(c=binary_rest,w)
boxplot(stars~c,data=ww,main="Boxplot of binary feature of Chinese category vs stars.", xlab="binary feature of Chinese category.",ylab="stars")

i=1
binary_rest = vector('integer');
for(cell in cat_col){
  if(grepl(cat3,cell)){
    binary_rest[i] = 1
  } else {
    binary_rest[i] = 0
  }   
  i=i+1
}
ww = cbind(d=binary_rest,w)
boxplot(stars~d,data=ww,main="Boxplot of binary feature of Fast Food category vs stars.", xlab="binary feature of Fast Food category.",ylab="stars")

range(w[,"likes"])