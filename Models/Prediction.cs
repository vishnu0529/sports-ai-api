namespace SportsAIPredictionAPI.Models;

public class Prediction
{
    public int Id { get; set; }
    public int UserId { get; set; }
    public int SportEventId { get; set; }
    public string PredictedOutcome { get; set; } = string.Empty;
    public double Confidence { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public User? User { get; set; }
    public SportEvent? SportEvent { get; set; }
}
