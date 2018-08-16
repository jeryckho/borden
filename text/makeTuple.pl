use strict;
use utf8;
use Data::Dumper;

my($text) = "Ceci est un test avec des accents hé à oui.";

my @Res;

for (my $idx = 0; $idx < 100; $idx ++) {
    for (my $idy = 0; $idy < 140; $idy ++) {
        $Res[$idx][$idy] = 0;
    }
}

my $List = {
    ' ' => 0,
    'a' => 1,
    'b' => 2,
    'f' => 3,
    'c' => 4,
    'j' => 5,
    'g' => 6,
    'p' => 7,
    'd' => 8,
    'm' => 9,
    'k' => 10,
    'q' => 11,
    'h' => 12,
    'r' => 13,
    's' => 14,
    'e' => 16,
    'o' => 17,
    'n' => 18,
    'w' => 19,
    'l' => 20,
    'x' => 21,
    't' => 22,
    'i' => 24,
    'y' => 25,
    'u' => 26,
    'z' => 27,
    'v' => 28,
    '?' => 29,
    ',' => 30,
    '.' => 31,
};

$text =~ y/A-Z/a-z/;
$text =~ y/èé/e/s;
$text =~ y/à/a/s;

# print $text;

my($X,$Y) = (1,1);

foreach my $char (split //, $text) {
    if (exists $List->{$char}){
        my(@lst) = dec2lst($List->{$char});
        # print "$char : [ $X , " . $Y . " ] <" .join('|', @lst) . "> " . ($#lst+1) . " \n";
        for (my $idz = 0;  $idz <= $#lst; $idz++) {
            $Res[ $X ][ $Y + $idz ] = $lst[$idz];
            # print ".";
        }
        $X++;
    } else {
        warn('oups ' . $char );
    }
}

print Dumper(\@Res);

exit();

sub dec2bin {
    my $str = unpack("B32", pack("N", shift));
    $str =~ s/^0+(?=\d)//;   # otherwise you'll get leading zeros
    return $str;
}
sub bin2dec {
    return unpack("N", pack("B32", substr("0" x 32 . shift, -32)));
}
sub dec2lst {
    my @res;
    my $str = unpack("B32", pack("N", shift));
    $str =~ s/^0+(?=\d)//;   # otherwise you'll get leading zeros
    foreach my $char (split //, $str) {
        unshift(@res, ($char eq "1"? 1 : 0 ));
    }
    return @res;
}
