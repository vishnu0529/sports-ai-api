using Microsoft.EntityFrameworkCore;
using SportsAIPredictionAPI.Models;

namespace SportsAIPredictionAPI.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<User> Users { get; set; }
    public DbSet<SportEvent> SportEvents { get; set; }
    public DbSet<Prediction> Predictions { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Prediction>()
            .HasOne(p => p.User)
            .WithMany()
            .HasForeignKey(p => p.UserId);

        modelBuilder.Entity<Prediction>()
            .HasOne(p => p.SportEvent)
            .WithMany()
            .HasForeignKey(p => p.SportEventId);
    }
}
