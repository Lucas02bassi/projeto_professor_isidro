import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int a, c;
        a = 2;
        System.out.print("Digite o valor de c: ");
        c = scanner.nextInt();
        c = ((c * a) - a);
        System.out.println(c);

    }
}
