// valac day04.vala

public class Aoc.Passport : HashTable<string, string>
{
    public Passport()
    {
	base(str_hash, str_equal);
    }

    public void print_all()
    {
	this.foreach ( (k,v) => {
	    stdout.printf("%s : %s\n", k, v);
	} );	    
    }

    public bool all_fields_present()
    {
	return this.get("byr") != null
	    && this.get("iyr") != null
	    && this.get("eyr") != null
	    && this.get("hgt") != null
	    && this.get("hcl") != null
	    && this.get("ecl") != null
	    && this.get("pid") != null;
    }

    private bool year_ok(string key, int low, int high)
    {
	string? value = this.get(key);
	if (value == null)
	    return false;

	var year = int.parse(value);
	return year >= low && year <= high;
    }

    private bool birth_year_ok()
    {
	return this.year_ok("byr", 1920, 2002);
    }

    private bool issue_year_ok()
    {
	return this.year_ok("iyr", 2010, 2020);
    }

    private bool expiration_year_ok()
    {
	return this.year_ok("eyr", 2020, 2030);
    }

    private bool height_ok()
    {
	string? value = this.get("hgt");
	if (value == null)
	    return false;

	// Needs units, either 'cm' or 'in'. If there are fewer than 3 
	// characters, then we can't have both a number and a unit, so fail.
	if (value.length < 3)
	    return false;

	int low = 0;
	int high = 0;
	if (value.strip().has_suffix("cm"))
	{
	    low = 150;
	    high = 193;
	}
	else if (value.strip().has_suffix("in"))
	{
	    low = 59;
	    high = 76;
	}
	else
	{
	    return false;
	}

	var meas = int.parse(value);
	return (meas >= low && meas <= high);
    }

    private bool hair_color_ok()
    {
	string? value = this.get("hcl");
	if (value == null)
	    return false;

	GLib.Regex exp = /^#[0-9a-f]{6}$/;
	GLib.MatchInfo m;
	exp.match(value, 0, out m);
	
	return m.matches();
    }

    private bool eye_color_ok()
    {
	string? value = this.get("ecl");
	if (value == null)
	    return false;

	GLib.Regex exp = /(amb|blu|brn|gry|grn|hzl|oth)/;
	GLib.MatchInfo m;
	exp.match(value, 0, out m);
	
	return m.matches();
    }

    private bool passport_id_ok()
    {
	string? value = this.get("pid");
	if (value == null)
	    return false;

	GLib.Regex exp = /^[0-9]{9}$/;
	GLib.MatchInfo m;
	exp.match(value, 0, out m);
	
	return m.matches();
    }
    
    public bool is_valid()
    {
	return this.birth_year_ok()
	    && this.issue_year_ok()
	    && this.expiration_year_ok()
	    && this.height_ok()
	    && this.hair_color_ok()
	    && this.eye_color_ok()
	    && this.passport_id_ok();
    }
}

public class Aoc.Day04
{
    public List<Passport> read_input_file()
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

	var passports = new List<Passport>();
	foreach (var pp in raw_passports)
	{
	    var map = new Passport();
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

    public void do_part_a(List<Passport> passports)
    {
	int num_valid = 0;
	foreach (var p in passports)
	{
	    if (p.all_fields_present())
		num_valid++;
	}

	stdout.printf("There are %d valid passports.\n", num_valid);
    }

    public void do_part_b(List<Passport> passports)
    {
	int num_valid = 0;
	foreach (var p in passports)
	{
	    if (p.is_valid())
		num_valid++;
	}

	stdout.printf("There are %d valid passports.\n", num_valid);
    }
}

int main(string[] args)
{
    var app = new Aoc.Day04();

    var passports = app.read_input_file();
        
    stdout.printf("Running part a:\n");
    app.do_part_a(passports);
    
    stdout.printf("Running part b:\n");
    app.do_part_b(passports);
    
    return 0;
}
