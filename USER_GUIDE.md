# Movie Finder - Complete User Guide

## Getting Started

### First Time Setup
1. Visit the application homepage
2. You'll see the main search interface with "Movie Finder" branding
3. Type a movie name (e.g., "Inception", "Avatar", "Pulp Fiction")
4. Click "Search" or press Enter
5. Browse recommendations that appear

## Main Features

### Search & Recommendations

**Finding Movies**
- Type at least 2 characters to see autocomplete suggestions
- Select from dropdown or type the full movie name
- Click Search button to get recommendations
- Results show instantly with beautiful cards

**What You See**
- Main movie details: title, rating, genre, release date, runtime
- Movie poster with smooth hover effects
- Overview/synopsis of the plot
- Star rating with visual bar indicator
- User reviews with sentiment analysis

### Recommended Movies Section

**Browsing Recommendations**
- Scroll down to see recommended movies in a grid
- Each card shows the movie poster
- Hover effects highlight movies with scale animation
- Click any recommendation to view its details
- See 10 personalized recommendations based on content similarity

**Movie Details**
- Beautiful glassmorphic design
- Responsive grid (4 columns on desktop, 2 on tablet, 1 on mobile)
- Quick action buttons: Add to Favorites, Share

### Cast & Crew

**Discovering Actors**
- See top 5-10 cast members in card format
- Actor profile photos with name and character
- Click any actor to see detailed information
- Modal view with:
  - Birthday and age
  - Place of birth
  - Full biography
  - Professional history

### User Reviews

**What Others Think**
- Real IMDB user reviews displayed
- Sentiment analysis: "Good" or "Bad" badges
- Color-coded sentiments (green for good, amber for bad)
- Helps decide if a movie is worth watching

### Genre/Category Browsing

**Browse by Genre**
1. Click "Browse Genres" button on home page
2. See all available movie categories
3. Choose a genre with emoji icons (Action ⚔️, Comedy 😄, etc.)
4. View all movies in that category
5. See trending movies at the top

**Available Genres**
- Action, Adventure, Animation
- Comedy, Crime, Documentary
- Drama, Family, Fantasy
- History, Horror, Music
- Mystery, Romance, Science Fiction
- Thriller, War, Western
- And more!

### Favorites System

**Save Your Favorites**
1. While viewing a movie, click "Add to Favorites" button
2. Button changes to "★ Added to Favorites"
3. Favorites are saved locally on your device
4. Click "My Favorites" button to view all saved movies
5. Click "Clear All" to remove all favorites

**Why Use Favorites**
- Create a personal watch list
- Never forget movies you want to watch
- Quickly reference your preferences
- Persistent across sessions

### Search History

**Track Your Searches**
1. Click "History" button on home page
2. See your last 20 movie searches
3. Click any movie to search for it again
4. Click "Remove" to delete from history
5. Use "Clear History" to wipe all entries

**History Features**
- Numbered list of searches
- Newest searches first
- Quick one-click re-search
- Saves time finding that movie again

### Sharing Movies

**Share with Friends**
1. While viewing a movie, click "Share" button
2. On mobile: Opens native share menu (WhatsApp, Twitter, etc.)
3. On desktop: Copies to clipboard automatically
4. Share includes movie title and app name
5. Friends can click link to view the same movie

**Share Options**
- Facebook, Twitter, WhatsApp, Telegram
- Email (with movie details)
- Copy to clipboard
- Generate shareable link

### AI Features (Optional)

**With OpenAI Configured**
- AI-generated movie summaries
- Explanation of why movie is recommended
- Mood/vibe description
- Enhanced recommendations
- Natural language movie insights

**Enable AI Features**
1. Get OpenAI API key (free tier available)
2. Add OPENAI_API_KEY to environment
3. Restart application
4. AI features automatically activate
5. See AI-powered content in recommendations

## Navigation Guide

### Home Page
```
┌─────────────────────────────────────────┐
│ 🎬 Movie Finder    [Browse Genres] [Favorites] [History]
├─────────────────────────────────────────┤
│                                         │
│  Search Box                             │
│  [Type Movie Name] [Search Button]      │
│                                         │
│  Quick Tips Section                     │
│  ✓ Type at least 2 characters           │
│  ✓ Select from dropdown                 │
│  ✓ View recommendations & reviews       │
│                                         │
└─────────────────────────────────────────┘
```

### Movie Details Page
```
┌─────────────────────────────────────────┐
│ [← Back to Search]                      │
├─────────────────────────────────────────┤
│  POSTER          │  MOVIE DETAILS       │
│  [Image]         │  Title: Inception    │
│                  │  Rating: 8.8/10      │
│                  │  [♥ Add] [Share]     │
│                  │  Genre: Sci-Fi       │
│                  │  Release: 2010       │
├─────────────────────────────────────────┤
│ ✨ Recommended For You                  │
│ [Card] [Card] [Card] [Card] [Card]      │
├─────────────────────────────────────────┤
│ 👥 Top Cast                             │
│ [Actor] [Actor] [Actor] [Actor] [Actor] │
├─────────────────────────────────────────┤
│ 💬 User Reviews                         │
│ "Great movie!" - Good                   │
│ "Confusing plot" - Bad                  │
└─────────────────────────────────────────┘
```

### Genre Browsing Page
```
┌─────────────────────────────────────────┐
│ [← Back to Search]                      │
├─────────────────────────────────────────┤
│ Browse All Genres                       │
│ ⚔️ Action    😄 Comedy    👻 Horror     │
│ 🗺️ Adventure 🎭 Drama     💕 Romance   │
│ 🎨 Animation ✨ Fantasy    🚀 Sci-Fi    │
├─────────────────────────────────────────┤
│ Movies in: Science Fiction              │
│ [🚀 Inception]  [🚀 Avatar]  [🚀 Tenet]│
│ [🚀 Dune]       [🚀 Matrix]  [🚀 Alien]│
└─────────────────────────────────────────┘
```

## Tips & Tricks

### Pro Tips
1. **Exact Spelling**: Use exact movie names for best results
2. **Try Autocomplete**: Let suggestions guide you
3. **Read Reviews**: Check user sentiments before watching
4. **Check Cast**: See if favorite actors are in the movie
5. **Save Favorites**: Build your personal watch list
6. **Share Smart**: Use share feature when recommending

### Troubleshooting

**Movie Not Found**
- Check spelling carefully
- Try with year (e.g., "Inception 2010")
- Use part of title if full title too long
- Browse by genre instead

**Recommendations Not Loading**
- Wait a few seconds
- Check internet connection
- Try different movie
- Refresh the page

**AI Features Not Working**
- Add OPENAI_API_KEY to environment
- Restart application
- Check API key is valid
- System still works without AI key

**Favorites Not Saving**
- Enable cookies in browser
- Check localStorage isn't full
- Try different browser
- Clear browser cache and try again

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Enter | Search for movie |
| Esc | Close modals/dialogs |
| ↑ ↓ | Navigate autocomplete |
| Click Movie | View details |
| Ctrl+C | Copy (after share click) |

## Mobile Experience

### Mobile Features
- One-column recommendation layout
- Touch-optimized buttons and cards
- Smooth scrolling
- Efficient loading
- Responsive images
- Bottom navigation on small screens

### Mobile Tips
1. Tap "Browse Genres" to explore
2. Swipe left/right through recommendations
3. Use native share button
4. Landscape mode for bigger view
5. Tap movie card to see full details

## Desktop Experience

### Desktop Features
- Multi-column grid layouts
- Keyboard navigation
- Hover animations
- Optimized spacing
- Full detail display

### Desktop Tips
1. Use keyboard shortcuts
2. Hover for previews
3. Right-click to open in new tab
4. Use browser back button
5. Bookmark favorite genres

## Data Privacy

### What's Stored Locally
- Favorite movies (browser storage)
- Search history (browser storage)
- Preferences (not shared)

### What's Sent to Server
- Movie search queries
- Recommendation requests
- Cast and review requests

### OpenAI Data
- Movie summaries cached locally
- No personal data sent to OpenAI
- Only movie-related info sent
- See privacy policy for details

## Frequently Asked Questions

**Q: Is my data private?**
A: Yes! Favorites and history are stored only on your device.

**Q: Can I download movies?**
A: No, this is a recommendation system only.

**Q: What if OpenAI API is down?**
A: System works fine without it - just no AI summaries.

**Q: How often are recommendations updated?**
A: Every search generates new recommendations.

**Q: Can I export my favorites?**
A: Currently stored locally - see GitHub for export feature.

**Q: Works offline?**
A: No, requires internet connection to fetch data.

**Q: Multiple devices?**
A: Each device has separate favorites/history.

**Q: Mobile app?**
A: Web app works on all devices - no app download needed.

## Getting Help

### Resources
- ENHANCEMENT_SUMMARY.md - What's new
- FEATURES.md - Feature descriptions
- SETUP_GUIDE.md - Setup instructions
- DEVELOPMENT.md - For developers
- Check GitHub issues/discussions

### Report Issues
- Document the problem clearly
- Include screenshots if possible
- Mention browser and device
- Share steps to reproduce
- Check existing issues first

---

**Enjoy discovering amazing movies with Movie Finder!**
