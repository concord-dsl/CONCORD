
public class FooClass {

	public int foo() {
		int a = 1;
		try {
		 int a = 1 / 0;
		} catch(ArithmeticException e) {
		 	System.out.println("You should not divide a number by zero");
		}
		return a;
	}
	
	public static String fooBar() {
		return "foobarstr";
	}
}
