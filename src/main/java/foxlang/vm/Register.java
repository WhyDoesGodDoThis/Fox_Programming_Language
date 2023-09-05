package foxlang.vm;

public class Register {
    private double sectionA;
    private double sectionB;

    public Register() {
        this.sectionA = 0.0;
        this.sectionB = 0.0;
    }

    public double getSectionA() {
        return this.sectionA;
    }

    public void setSectionA(double sectionA) {
        this.sectionA = sectionA;
    }

    public double getSectionB() {
        return this.sectionB;
    }

    public void setSectionB(double sectionB) {
        this.sectionB = sectionB;
    }
}
