// valac day03.vala

class Aoc.Day03
{
    private List<string> read_input_file()
    {
	FileStream stream = FileStream.open("./input.txt", "r");
	assert (stream != null);

	var list = new List<string>();
	string? line = null;
	while ((line = stream.read_line()) != null)
	{
	    var stripped = line.strip();
	    if (stripped.length == 0)
	    {
		stdout.printf("Glarg");
	    }
	    list.append(stripped);
	}
	
	return list;
    }
    
    public void do_part_a()
    {
	var map = this.read_input_file();
	var num_rows = map.length();
	var unit_width = map.nth_data(0).length;

	int x_pos = 0;
	int y_pos = 0;
	int delta_x = 3;
	int delta_y = 1;
	int num_trees = 0;

	while (true)
	{
	    x_pos = (x_pos + delta_x) % unit_width;
	    y_pos = y_pos + delta_y;

	    if (y_pos >= num_rows)
		break;
		
	    var new_space = map.nth_data(y_pos).get_char(x_pos);
	    if (new_space == '#')
		num_trees++;
	}

	stdout.printf("Ran into %d trees.\n", num_trees);
    }

    public void do_part_b()
    {
    }
}

int main(string[] args)
{
    var app = new Aoc.Day03();

    stdout.printf("Running part a:\n");
    app.do_part_a();
    
    stdout.printf("Running part b:\n");
    app.do_part_b();
    
    return 0;
}
