// valac day02.vala

class Aoc.Day02
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
	    list.append(stripped);
	}
	
	return list;
    }

    private int count(string str, unichar target)
    {
	int instances = 0;
	unichar c;
	for (int i = 0; str.get_next_char(ref i, out c);)
	{
	    if (c == target)
		instances++;
	}
	
	return instances;
    }
    
    public void do_part_a()
    {
	var all_lines = read_input_file();

	int passes = 0;
	int failures = 0;

	foreach (var line in all_lines)
	{
	    GLib.Regex exp = /^\s*([0-9]+)\s*-\s*([0-9]+)\s*([a-zA-Z])\s*:\s*([a-zA-Z]+)\s*$/;

	    try
	    {
		GLib.MatchInfo m;
		for (exp.match(line, 0, out m); m.matches(); m.next())
		{
		    var low = int.parse(m.fetch(1));
		    var high = int.parse(m.fetch(2));
		    var letter = m.fetch(3).get_char(0);
		    var password = m.fetch(4);

		    // get number of instances of letter in password
		    var num_target_letter = this.count(password, letter);
		    if (num_target_letter >= low && num_target_letter <= high)
			passes++;
		    else
			failures++;
		}
	    }
	    catch (GLib.Error e)
	    {
		GLib.error("Regex failed: %s", e.message);
	    }
        }

	stdout.printf("There were %d valid passwords and %d invalid passwords\n", passes, failures);
    }

    public void do_part_b()
    {
	var all_lines = read_input_file();

	int passes = 0;
	int failures = 0;

	foreach (var line in all_lines)
	{
	    GLib.Regex exp = /^\s*([0-9]+)\s*-\s*([0-9]+)\s*([a-zA-Z])\s*:\s*([a-zA-Z]+)\s*$/;

	    try
	    {
		GLib.MatchInfo m;
		for (exp.match(line, 0, out m); m.matches(); m.next())
		{
		    var idx1 = int.parse(m.fetch(1));
		    var idx2 = int.parse(m.fetch(2));
		    var letter = m.fetch(3).get_char(0);
		    var password = m.fetch(4);

		    // The indices in the file are 1-indexed, not 0-indexed,
		    // so we convert to 0-indexed values here.
		    idx1--;
		    idx2--;

		    var idx1_valid = password.length > idx1 && password.get_char(idx1) == letter;
		    var idx2_valid = password.length > idx2 && password.get_char(idx2) == letter;
		    
		    if ((idx1_valid && !idx2_valid) || (!idx1_valid && idx2_valid))
			passes++;
		    else
			failures++;
		}
	    }
	    catch (GLib.Error e)
	    {
		GLib.error("Regex failed: %s", e.message);
	    }
        }

	stdout.printf("There were %d valid passwords and %d invalid passwords\n", passes, failures);
    }
}

int main(string[] args)
{
    var app = new Aoc.Day02();
    
    stdout.printf("Running part a:\n");
    app.do_part_a();

    stdout.printf("Running part b:\n");
    app.do_part_b();
    
    return 0;
}
