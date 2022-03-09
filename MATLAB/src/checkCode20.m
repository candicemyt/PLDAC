function [pass] = checkCode20(imc)

disp(imc)
im = imc(:,1:2);
check1_1 = imc(:,3);
disp(check1_1);
disp(length(check1_1));
check1_2 = imc(1:2,4);
disp(check1_2);
disp(length(check1_2));
check1 = [check1_1 : check1_2];
check2_1 = imc(:,5);
check2_2 = imc(3:4,4);
check2 = [check2_1 : check2_2];
tmp = [];
%on teste les lignes
for bb = 1:2
    if mod(sum(im(:,bb)),2)==check1(bb)
        tmp(bb) = 0;
    else
        tmp(bb) = 1;
    end
end
%on teste les colonnes
for bb = 1:4
    if mod(sum(im(bb,:)),2)==check1(2+bb)
        tmp(2+bb) = 0;
    else
        tmp(2+bb) = 1;
    end
end
    
cor = sum(check1 == fliplr(check2));
 if  cor==6
     tmp(7) = 0;
 else tmp(7) = 1;
 end
    
if(sum(tmp)) > 0
    pass = 0;
else pass = 1;
    
end



end