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

    private int get_num_trees(List<string> map, int dx, int dy)
    {
	var num_rows = map.length();
	var unit_width = map.nth_data(0).length;

	int x_pos = 0;
	int y_pos = 0;
	int num_trees = 0;

	while (true)
	{
	    x_pos = (x_pos + dx) % unit_width;
	    y_pos = y_pos + dy;

	    if (y_pos >= num_rows)
		break;
		
	    var new_space = map.nth_data(y_pos).get_char(x_pos);
	    if (new_space == '#')
		num_trees++;
	}

	return num_trees;
    }
    
    public void do_part_a()
    {
	var map = this.read_input_file();
	var num_rows = map.length();
	var unit_width = map.nth_data(0).length;

	int delta_x = 3;
	int delta_y = 1;

	var num_trees = get_num_trees(map, delta_x, delta_y);

	stdout.printf("Part b: %llu\n", num_trees);
    }

    public void do_part_b()
    {
	var map = this.read_input_file();
	int[,] slopes_to_try = {{1,3,5,7,1},
				{1,1,1,1,2}};
	var num_slopes = slopes_to_try.length[1];
	uint64 product = 1;

	for (var slope_idx = 0; slope_idx < num_slopes; slope_idx++)
	{
	    var delta_x = slopes_to_try[0, slope_idx];
	    var delta_y = slopes_to_try[1, slope_idx];
	    product = product * get_num_trees(map, delta_x, delta_y);
        }

	stdout.printf("Final product: %llu\n", product);
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
