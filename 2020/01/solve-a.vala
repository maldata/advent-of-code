using Gee;

class Aoc.Day1 : GLib.Object
{
    public void do_part_a()
    {
	stdout.printf("Inside part a:\n");

	var list = new ArrayList<int> ();
	list.add (1);
	list.add (2);
	list.add (5);
	list.add (4);
	


	
    }
    
    public void do_part_b()
    {
	stdout.printf("Inside part b:\n");
    }
}

public static int main(string[] args)
{
    var app = new Aoc.Day1();
    
    stdout.printf("Running part a:\n");
    app.do_part_a();
    
    stdout.printf("Running part b:\n");
    app.do_part_b();
    
    return 0;
}
