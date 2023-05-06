
public class RemovableStatements {
	
	public void ifStatementMethod(int a) {
		int p = 1;
		int ab = foo();
		
		if(p > 1) {
			System.out.println("True");
			System.exit(0);
		}

		int[] array = new int[]{1, 2, 5, 77};

		for (int i = 0; i < array.length; i++) {
			if(i % 2 == 0) System.out.println(i);
		}
		
		System.out.println("False");
		
		while(p >= 0) {
			System.out.println(p);
			p--;
		}
		try {
		 int ak = 1 / p;
		} catch(ArithmeticException e) {
		 	System.out.println("You should not divide a number by zero");
			 System.out.printf("Hello %s!%n", "World");
		}
	}
	
	public void blockStatementMethod() {
		int p = 1;
		switch (p) {
		case 1: {
			
			System.out.println("One");
		}
		case 2: {
			System.out.println("Two");
		}
		default:
			throw new IllegalArgumentException("Unexpected value: " + p);
		}
	}
	
	public int foo() {
		int a = 1;
		int b = 2;
		
		return a+b;
	}
}
