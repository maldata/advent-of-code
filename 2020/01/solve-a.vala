// valac --pkg glib-2.0 solve-a.vala

class Aoc.Day1 : GLib.Object
{
    public void do_part_a()
    {
	var list = this.read_input_file();
	foreach(var l in list)
	{
	    stdout.printf("%d\n", l);
        }
    }
    
    public List<int> read_input_file()
    {
	stdout.printf("Inside part a:\n");

	FileStream stream = FileStream.open("./input.txt", "r");
	assert (stream != null);

	var list = new List<int>();
	string? line = null;
	while ((line = stream.read_line()) != null)
	{
	    var stripped = line.strip();
	    list.append(int.parse(stripped));
	}
	
	return list;
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
