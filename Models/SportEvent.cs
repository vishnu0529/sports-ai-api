namespace SportsAIPredictionAPI.Models;

public class SportEvent
{
    public int Id { get; set; }
    public string Sport { get; set; } = string.Empty;
    public string HomeTeam { get; set; } = string.Empty;
    public string AwayTeam { get; set; } = string.Empty;
    public DateTime EventDate { get; set; }
    public string Status { get; set; } = "Upcoming";
}
