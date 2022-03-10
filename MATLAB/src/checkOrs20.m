function [passBin codesFinal orientation codes] = checkOrs(imc)

check = [];
passBin = [];
codes = [];

cc = 1;
%imcr = rot90(imc,cc);
check(cc) = checkCode20(imc);
codes(cc,:) = reshape(imcr', 1 ,20);
cc = 2;
imcr = rot90(imc,cc);
check(2) = checkCode20(imcr);
codes(2,:) = reshape(imcr', 1 ,20);

if sum(check)~=1
    passBin = 0;
elseif sum(check) == 1
    passBin=1;
end

codesFinal = codes(find(check==1),:);
orientation = find(check ==1);

end
