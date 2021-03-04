// valac --pkg glib-2.0 solve-a.vala

class Aoc.Day1 : GLib.Object
{
    private List<int> read_input_file()
    {
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
    
    public void do_part_a()
    {
	var list = this.read_input_file();
	var found = false;
	var complement = 0;
	var diff = 0;
	foreach(var l in list)
	{
	    complement = 2020 - l;
	    if (list.index(complement) >=0)
	    {
		found = true;
		diff = l;
		break;
	    }
        }

	if (!found)
	{
	    stdout.printf("Something went horribly wrong!\n");
	}
	else
	{
	    stdout.printf("%d * %d = %d\n", diff, complement, diff * complement);
	}
    }

    private void find_pair(List<int> list, int target, out int? a, out int? b, out bool found)
    {
	found = false;
	a = null;
	b = null;
	if (list.length() == 0)
	    return;

	foreach(var l in list)
	{
	    var complement = target - l;
	    if (list.index(complement) >=0)
	    {
		a = l;
		b = complement;
		found = true;
	    }
	}
    }
    
    public void do_part_b()
    {
	var list = this.read_input_file();
	var triplet_found = false;
	foreach(var l in list)
	{
	    var remainder = 2020 - l;
        }
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
