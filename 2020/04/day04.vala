// valac day04.vala

public class Aoc.Day04
{
    public List<HashTable<string, string>> read_input_file()
    {
	string file_contents;
	string[] raw_passports = null;
	try
	{
	    FileUtils.get_contents("./input.txt", out file_contents);
	    raw_passports = file_contents.split("\n\n");
	}
	catch (GLib.FileError e)
	{
	    stdout.printf("Error: %s\n", e.message);
	}

	var passports = new List<HashTable<string, string>>();
	foreach (var pp in raw_passports)
	{
	    var map = new HashTable<string, string>(str_hash, str_equal);
	    string[] exploded = pp.replace(" ", "\n").split("\n");
	    foreach (var element in exploded)
	    {
		var stripped = element.strip();
		if (stripped != "")
		{
		    var kv = element.split(":");
		    map.insert(kv[0], kv[1]);
		}
	    }
	    passports.append(map);
	}

	return passports;
    }
    
    public void do_part_a(List<HashTable<string, string>> passports)
    {
	int num_valid = 0;
	foreach (var p in passports)
	{
	    p.foreach ( (k,v) => {
		stdout.printf("%s : %s\n", k, v);
	    } );
	    stdout.printf("---------\n");
	}
    }

    public void do_part_b()
    {
    }
}

int main(string[] args)
{
    var app = new Aoc.Day04();

    var passports = app.read_input_file();
        
    stdout.printf("Running part a:\n");
    app.do_part_a(passports);
    
    stdout.printf("Running part b:\n");
    app.do_part_b();
    
    return 0;
}
