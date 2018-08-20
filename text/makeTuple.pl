use strict;
use utf8;
use Data::Dumper;

our($text);
require "text.pl"; 

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
    '.' => 32,
    "'" => 33,
    '!' => 36,
    '?' => 40,
    ',' => 48,
};

$text =~ y/A-Z/a-z/;
$text =~ y/àâä/a/s;
$text =~ y/èéêë/e/s;
$text =~ y/ô/o/s;
$text =~ y/ù/u/s;
$text =~ y/ç/c/s;
$text =~ y/;/,/s;
$text =~ y/’/'/s;
$text =~ y/-/ /s;

my( $X, $Y ) = ( 1, 1 );
my( $MaxX, $DeltaY ) = ( 98, 8 );
my( $Sens ) = 1;

foreach my $word (split / +/, $text) {
    if (($X + $Sens*(length $word)) > $MaxX) {
        $X = $MaxX;
        $Y += $DeltaY;
        $Sens *= -1;
    } elsif (($X + $Sens*(length $word)) < 1) {
        $X = 1;
        $Y += $DeltaY;
        $Sens *= -1;
    }
    foreach my $char (split //, $word) {
        if (exists $List->{$char}){
            my(@lst) = dec2lst($List->{$char});
            for (my $idz = 0;  $idz <= $#lst; $idz++) {
                $Res[ $X ][ $Y + $idz ] = $lst[$idz];
            }
            $X += $Sens;
            if ($X >= $MaxX) {
                $X = $MaxX;
                $Y += $DeltaY;
                $Sens *= -1;
            } elsif ($X <= 1) {
                $X = 1;
                $Y += $DeltaY;
                $Sens *= -1;
            }
        } else {
            warn('oups ' . $char );
        }
    }
    $X += $Sens;
}

my @Ligs = ();
for (my $idy = 0; $idy < 140; $idy ++) {
    my(@Loc);
    for (my $idx = 0; $idx < 100; $idx ++) {
        push( @Loc, $Res[$idx][$idy]);
    }
    push( @Ligs, "\t(" . join(',', @Loc) . ')' );
}
print "TX = (\n". join(",\n", @Ligs) . "\n)\n";

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
