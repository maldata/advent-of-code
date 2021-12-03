// valac --pkg glib-2.0 solutions.vala

public class Move
{
    public string direction;
    public int quantity;

    public Move(string d, int q)
    {
        this.direction = d;
        this.quantity = q;
    }
}

public static Array<Move> read_moves()
{
    FileStream stream = FileStream.open("./input.txt", "r");
    assert (stream != null);

    var all_moves = new Array<Move>();
    string? line = null;

    while ((line = stream.read_line()) != null)
    {
        var stripped_line = line.strip();
        var split_line = stripped_line.split(" ", 2);
        var m = new Move(split_line[0], int.parse(split_line[1]));
        all_moves.append_val(m);
    }

    return all_moves;
}

public void solve_a(Array<Move> moves)
{
    int horizontal_pos = 0;
    int depth = 0;

    for (int i = 0; i < moves.length ; i++)
    {
        var m = moves.index(i);

        if (m.direction == "forward")
            horizontal_pos = horizontal_pos + m.quantity;
        else if (m.direction == "down")
            depth = depth + m.quantity;
        else if (m.direction == "up")
            depth = depth - m.quantity;
        else
            stdout.printf("I don't know what to do with '%s'\n", m.direction);
	}

    stdout.printf("Final horizontal position and depth: %d and %d.\n", horizontal_pos, depth);
    stdout.printf("Product of horizontal position and depth: %d\n", horizontal_pos * depth);
}

public void solve_b(Array<Move> moves)
{
    int horizontal_pos = 0;
    int depth = 0;
    int aim = 0;

    for (int i = 0; i < moves.length ; i++)
    {
        var m = moves.index(i);

        if (m.direction == "forward")
        {
            horizontal_pos = horizontal_pos + m.quantity;
            depth = depth + aim * m.quantity;
        }
        else if (m.direction == "down")
            aim = aim + m.quantity;
        else if (m.direction == "up")
            aim = aim - m.quantity;
        else
            stdout.printf("I don't know what to do with '%s'\n", m.direction);
	}

    stdout.printf("Final horizontal position and depth: %d and %d.\n", horizontal_pos, depth);
    stdout.printf("Product of horizontal position and depth: %d\n", horizontal_pos * depth);
}

public static int main (string[] args)
{
    var moves = read_moves();
    solve_a(moves);
    solve_b(moves);

    return 0;
}
