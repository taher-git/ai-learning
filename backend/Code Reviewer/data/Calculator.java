// File: Calculator.java
// Basic calculator implementation (for code review practice)

import java.util.Scanner;

public class Calculator {

    // Adds two numbers
    public double add(double x, double y){
        return x + y; // ok
    }

    // subtracts two numbers (but inconsistent naming)
    public double Subtract(double a, double b){ // Naming inconsistent (capital S)
        return a-b;
    }

    // multiply method - could be static but isn’t
    public double multiply(double n1, double n2){
        double result = n1 * n2;
        System.out.println("Multiplying..."); // Unnecessary side effect
        return result;
    }

    // divide method - poor handling of division by zero
    public double divide(double n1, double n2){
        if(n2 == 0){
            System.out.println("Cannot divide by zero! Returning 0.");
            return 0; // should throw exception instead
        }
        return n1 / n2;
    }

    // Calculates power but with integer cast issue
    public double pow(double base, double exp){
        int e = (int)exp; // casts exponent to int even if not intended
        return Math.pow(base, e);
    }

    // Calculates square root but doesn’t check for negatives properly
    public double sqrt(double num){
        if(num == 0){
            return 0; // handles 0 only
        }
        return Math.sqrt(num); // ignores negatives
    }

    // Unnecessary repetition - calculates average using other methods
    public double average(double a, double b){
        double sum = add(a, b);
        double div = divide(sum, 2);
        return div;
    }

    // main method does both calculation and user input (mixes logic and I/O)
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        Calculator c = new Calculator();

        System.out.print("Enter first number: ");
        double n1 = sc.nextDouble();
        System.out.print("Enter second number: ");
        double n2 = sc.nextDouble();

        System.out.println("Add: " + c.add(n1, n2));
        System.out.println("Subtract: " + c.Subtract(n1, n2));
        System.out.println("Multiply: " + c.multiply(n1, n2));
        System.out.println("Divide: " + c.divide(n1, n2));
        System.out.println("Power: " + c.pow(n1, n2));
        System.out.println("Average: " + c.average(n1, n2));
        System.out.println("Square Root (first num): " + c.sqrt(n1));
    }
}
