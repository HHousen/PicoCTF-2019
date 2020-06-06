Java.perform(function() {
    console.log("Injecting new getFlag()...");
    var classFlagstaff;

    classFlagstaff = Java.use("com.hellocmu.picoctf.FlagstaffHill");
    classFlagstaff.getFlag.implementation = function(input, ctx) {
        console.log("Entered getFlag() function");
        var flag = classFlagstaff.cardamom(input);
        console.log("GOT FLAG: " + flag)
        return flag;
    };
});