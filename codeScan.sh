
dir=${HOME}/Documents/YYCode/haokan-ios/Pods/
components=(
    yybaseapisdk
    yybaseservice
    yychannelmodules
    yydocumentcomponent-ios
    yyfeedbackcomponent
    yygiftviewcomponent
    yyiapcomponent
    yymediatorsdk
    yyreportcomponent
    yywebcomponent
    BDGameTplComponent
)

paths=''
out=${HOME}/Downloads/diff.txt
for c in "${components[@]}"
do
paths=$paths$dir$c","
done
paths=`echo ${paths%?}`
echo $paths
python3 checkDiffProtocol.py $paths $out