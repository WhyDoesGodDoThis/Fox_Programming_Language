package foxlang;

public final class Constants {
    public static interface opcodes {
        public static final byte LOAD = 1;
        public static final byte MOVE = 2;
        public static final byte STACK = 3;
        public static final byte TAKE = 4;
        public static final byte COLLAPSE = 5;
        public static final byte JUMP = 6;
        public static final byte JUMP_IF = 7;
        public static final byte JUMP_IF_ZERO = 8;
        public static final byte JUMP_IF_NOT = 9;
        public static final byte CLEAR = 10;
        public static final byte CYCLE = 11;
        public static final byte END = 127;
        public static final byte LABEL = 126;
    }
}
