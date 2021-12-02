// valac --pkg glib-2.0 solutions.vala

public static List<int> read_depths()
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

public static void solve_a(List<int> depths)
{
    var num_increases = 0;
    for (var i = 1; i < depths.length(); i++)
    {
        if (depths.nth_data(i) > depths.nth_data(i-1))
            num_increases++;
    }

    stdout.printf("The depth increases %d times.\n", num_increases);
}

public static void solve_b(List<int> depths, int window_size)
{
    var num_windows = depths.length() - window_size + 1;
    var window_sums = new List<int>();

    for (var i = 0; i < num_windows; i++)
    {
        var sum = 0;
        for (var j = 0; j < window_size; j++)
        {
            var idx = i + j;
            sum = sum + depths.nth_data(idx);
        }

        window_sums.append(sum);
    }

    solve_a(window_sums);
}

public static int main(string[] args)
{
    var depths = read_depths();
    solve_a(depths);
    solve_b(depths, 3);    

    return 0;
}
