# Omsæt Gravsoft grid til GDAL-kompatibel XYZ
#
# NB: Ofte er Gravsoft grid headere skrevet med manglende
# opløsning i skridtværdierne. Det har derfor været nødvendigt
# at rette "0.01666667" og lignende til "0.016666666666666666666666666667"
# for at gdal_translate kan finde ud af sagerne.
#
# Eksempelopskrift: Gravsoft til GeoTIFF
#
#     gawk -f gravsoft2xyz.awk absg.grd > absg.xyz
#     gdal_translate absg.xyz absg.tif
#
# Check:
#     gdalinfo absg.tif
#     gdallocationinfo -geoloc absg.tif 7.7 58
#         (expect 1.6507)
#     gdallocationinfo -geoloc -valonly absg.tif 7.800001 58
#         (expect 1.6825)
#     gdallocationinfo -geoloc -valonly absg.tif 13.00001 58
#         (expect 3.4505)
#     gdallocationinfo -geoloc -valonly absg.tif 13.00001 54.1
#         (expect 0.1601)
#     gdallocationinfo -geoloc -valonly absg.tif 7.7 54.1
#         (expect -0.2361)
#
#
# Thomas Knudsen, SDFI, <thokn@sdfi.dk>, 2023-05-03
#

# Postadskiller er en vilkårlig følge af blanktegn
# (herunder linjeskift)
BEGIN {
    RS="[[:space:]]+"
    OFMT = "%14.9f"
    print "x y z"
    # NR = 0
}

# Fortolk headerinformationer, som udgør de 6 første tal i filen.
# Men første post (NR==1) er tom, fordi filen indledes med blanktegn.
# Derfor har de 6 første tal post-indeks 2 til 7, ikke 1 til 6.
NR==1 { next }
NR==2 { S  = $1 + 0.; next }
NR==3 { N  = $1 + 0.; next }
NR==4 { W  = $1 + 0.; next }
NR==5 { E  = $1 + 0.; next }
NR==6 { dn = $1 + 0.; next }
NR==7 {
    de = $1 + 0.

    row = 0
    rows = int( (N - S) / dn + 1.5)

    col = 0
    cols = int( (E - W) / de + 1.5)

    knot = 0
    knots = rows * cols

    x = W + 0.
    y = N + 0.

    print N, S, E, W, dn, de, rows, cols > "/dev/stderr"
    next
}

{
    printf("%14.9f %14.9f %s\n", x, y, $0)

    knot += 1
    col += 1
    x += de


    # End-of-row? Wrap around columns and step one row down
    if (col == cols) {
        # print x " " y " " $0 " " knot " " knot%col > "/dev/stderr"
        print ""
        row += 1
        col = 0
        x = W + 0.
        y -= dn
    }

}


END {
    if (knot != knots) {
        print "Expected " knots " got " knot > "/dev/stderr"
    }
}
