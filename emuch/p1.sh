# get 'f=' values
grep -n 'Excited State' 1.txt > state.txt
awk '{sub(/f=/,"");print $9}' state.txt > fvalue.txt

# get line numbers of the begin and the end of 'Excited State' lines
# Note that the last 'Excited State' lines end with "Li@..." which differs from others, others end with a blank line.
awk '
BEGIN{
	bState=0;
	nState=0;
}
{
	if(match($1,"Excited")){
		nState+=1;
		bState=1;
		begin[nState]=NR
	}
	if(NR>begin[nState] && bState==1){
		if($0==""){  
			bState=0;
			end[nState]=NR
		}
		if(match($0,"Li")){
			bState=0;
			end[nState]=NR-1
		}
	}
}
END{
	if(nState>0){
		for(i=1;i<=nState;++i)
		{
			printf ("%s  %s\n",begin[i],end[i]);
		}
	}
	else {
		printf ("Excited State not found!\n");
	}
}
' 1.txt > lines.txt

# get the lines contains maximum value (and 2nd value if maximum - 2nd < 0.01)
paste fvalue.txt lines.txt > p1_1.txt
awk '
BEGIN{
	f_max=0;
	f_2nd=0;
	printf("Part 1:\n");	
}
{
	if(NR==FNR){
		if($1>f_max){
			f_max = $1;
			begin_max = $2;
			end_max = $3;
		}
		else {
			if(f_max-$1<0.01){
				f_2nd = $1;
				begin_2nd = $2;
				end_2nd = $3;
			}
		}
	}
}
{
	if(NR>FNR){
		if(f_max>0){
			if(begin_max <= FNR && FNR <= end_max) {
				print $0;
			}
		}
		if(f_2nd>0){
			if(begin_2nd <= FNR && FNR <= end_2nd) {
				print $0;
			}		
		}
	}
}
END{
}
' p1_1.txt 1.txt > p1.txt

# remove files not needed
rm state.txt 
rm fvalue.txt
rm lines.txt
rm p1_1.txt
