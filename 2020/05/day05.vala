// valac day05.vala

public class Aoc.Day05
{
    public int bin_str_to_num(string s, unichar z, unichar o)
    {
	int value = 0;
	unichar c;
	
	for (int i = 0; s.get_next_char(ref i, out c);)
	{
	    if (c == z)
		value = value * 2;
	    else if (c == o)
		value = (value * 2) + 1;
	    else
	    {
		stdout.printf("Error: no %s in %s\n", c.to_string(), s);
		return 0;
	    }
	}
	
	return value;
    }
    
    public List<string> read_input_file()
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
    
    public void do_part_a(List<string> codes)
    {
    	int highest_id = 0;

	foreach (var code in codes)
	{
	    var row_code = code.substring(0, 7);
	    var seat_code = code.substring(7, -1);

	    var row_number = bin_str_to_num(row_code, 'F', 'B');
	    var seat_number = bin_str_to_num(seat_code, 'L', 'R');
	    var seat_id = (row_number * 8) + seat_number;
	    
	    highest_id = int.max(highest_id, seat_id);
	}

	stdout.printf("The highest seat ID is %d\n", highest_id);
    }
    
    public void do_part_b(List<string> codes)
    {

 /*
    lowest_id = 2**10
    highest_id = 0
    all_ids = []
    for code in codes:
        row_code = code[:7]
        seat_code = code[7:]

        row_number = bin_str_to_num(row_code, 'F', 'B')
        seat_number = bin_str_to_num(seat_code, 'L', 'R')
        seat_id = (row_number * 8) + seat_number
        all_ids.append(seat_id)
        
        lowest_id = min(lowest_id, seat_id)
        highest_id = max(highest_id, seat_id)

    print('The lowest seat ID is {0}'.format(lowest_id))
    print('The highest seat ID is {0}'.format(highest_id))

    all_ids.sort()

    for i, j in enumerate(all_ids):
        if i == 0 or i == len(all_ids) - 1:
            continue

        if all_ids[i-1] == j - 1 and all_ids[i+1] == j + 1:
            continue

        print('Found a gap at index {0}.'.format(i))
        print(all_ids[i-1:i+1])

*/
    }
}

int main(string[] args)
{
    var app = new Aoc.Day05();

    var codes = app.read_input_file();
    
    stdout.printf("Running part a:\n");
    app.do_part_a(codes);
    
    stdout.printf("Running part b:\n");
    app.do_part_b(codes);
    
    return 0;
}
