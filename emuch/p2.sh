# get the log from input file
awk '
BEGIN{
	bLog=0;
	lines=0;
	strLog="";
}
{
	if(match($1,"\"Li")){
		bLog=1;
		nLog=NR;
	}
	if(NR>nLog && bLog==1){
		if(!match($1,"Job")){
			lines+=1;
			str[lines]=$0;
		}
		else {
			bLog=0;
		}
	}
}
END{
	if(lines>0){
		for(i=1;i<lines;++i)
			strLog = strLog""str[i]
	}
	print strLog
}
' 1.txt > p2_log.txt

# change log separate character from "\\" to "\n"
awk '
BEGIN{
	FS="\\"
}
{
	for(i=1;i<=NF;++i)
	{
		print $i;
	}
}
END{
}
' p2_log.txt > p2_sep.txt

# get HF and Polar line
awk '
BEGIN{
	FS="=";
	nHF=0;
}
{
	if($1=="HF"){
		nHF += 1;
		hf_value[nHF]=$2;
	}
	if($1=="Polar"){
		polar_values=$2;
	}
}
END{
	printf("HF,%s\n",hf_value[nHF]);     # you can print every HF within a loop if you wish
	printf("Polar,%s\n",polar_values);
}
' p2_sep.txt > p2_data.txt

# print HF and alpha value
awk '
BEGIN{
	FS=","
}
{
	if($1=="HF"){
		printf("\nPart 2:\n");
		printf("HF = %s\n",$2);
	}
	if($1=="Polar"){
		printf("\nPart 3:\n");
		if(NF<7){
			printf("Number of polar values < 6, please check input\n");
		}
		else {
			printf("Alpha = %12.8f\n",($2+$4+$7)/3.0);
		}
	}
}
END{
}
' p2_data.txt > p2p3.txt

# clean
rm p2_log.txt
rm p2_sep.txt
rm p2_data.txt
