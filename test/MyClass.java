import java.io.*;
import java.util.HashMap;
import java.util.Map;

public class MyClass implements ScriptBasic {

    // FIELDS
    private final String assigned = "some string";
    private Reader input; // not finap
    private final Writer output;
    final private Writer error;
    // does not get value, but it is static, it will get value in some static block, we do not care
    final static private boolean theMapHasToBeFilled;
    public Context ctx; // public
    // END

    // CONSTRUCTOR
    public MyClass(final Writer output, final Writer error) {
        this.output = output;
        this.error = error;
    }
    // END

    // GETTERS
    // END

    // SETTERS
    // END

    // EQUALS
    // END
}