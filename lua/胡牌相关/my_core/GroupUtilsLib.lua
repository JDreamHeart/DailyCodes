local GroupUtilsLib = {};

function GroupUtilsLib:findSame(byte,cardByte)
    return byte == cardByte;
end

function GroupUtilsLib:findShun(byte,cardByte)
    return cardByte == (byte + 1);
end

return GroupUtilsLib;