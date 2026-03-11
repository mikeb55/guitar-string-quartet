\version "2.24" 
\include "lilypond-book-preamble.ly"
    
color = #(define-music-function (parser location color) (string?) #{
        \once \override NoteHead #'color = #(x11-color color)
        \once \override Stem #'color = #(x11-color color)
        \once \override Rest #'color = #(x11-color color)
        \once \override Beam #'color = #(x11-color color)
     #})
    
\header { 
 title = "Sylva Narrative No.2"   
  
  } 
 
\score  { 
 
      << \new Staff  = ycxycexcbdwya { \key d \major 
             \time 5/4
             r 1  
             s 4  
             \bar "|"  %{ end measure 1 %} 
             r 1  
             s 4  
             \bar "|"  %{ end measure 2 %} 
             r 1  
             s 4  
             \bar "|"  %{ end measure 3 %} 
             r 1  
             s 4  
             \bar "|"  %{ end measure 4 %} 
             a' 2  
             r 8  
             fis' 4.  
             r 4  
             \bar "|"  %{ end measure 5 %} 
             b' 4.  
             r 4  
             g' 8  
             r 2  
             \bar "|"  %{ end measure 6 %} 
             a 4.  
             r 4  
             d' 8  
             r 2  
             \bar "|"  %{ end measure 7 %} 
             d' 2  
             r 8  
             b 4.  
             r 4  
             \bar "|"  %{ end measure 8 %} 
             a' 4.  
             r 4  
             a' 8  
             r 2  
             \bar "|"  %{ end measure 9 %} 
             b' 2  
             r 8  
             b' 4.  
             r 4  
             \bar "|"  %{ end measure 10 %} 
             b' 4.  
             r 4  
             a' 8  
             r 2  
             \bar "|"  %{ end measure 11 %} 
             a' 2  
             r 8  
             e' 4.  
             r 4  
             \bar "|"  %{ end measure 12 %} 
             fis' 2  
             r 8  
             a 4.  
             r 4  
             \bar "|"  %{ end measure 13 %} 
             b' 4.  
             r 4  
             b' 8  
             r 2  
             \bar "|"  %{ end measure 14 %} 
             e' 2  
             r 8  
             d' 4.  
             r 4  
             \bar "|"  %{ end measure 15 %} 
             cis'' 4.  
             r 4  
             e' 8  
             r 2  
             \bar "|"  %{ end measure 16 %} 
             b' 2  ~  
             b' 8  
             r 16  
             d' 16  
             r 2  
             \bar "|"  %{ end measure 17 %} 
             e'' 4  
             r 4  
             e'' 4  
             r 2  
             \bar "|"  %{ end measure 18 %} 
             g' 8  
             r 2  
             gis' 4  
             r 4.  
             \bar "|"  %{ end measure 19 %} 
             e'' 2  ~  
             e'' 8  
             r 16  
             gis' 16  
             r 2  
             \bar "|"  %{ end measure 20 %} 
             b' 4  
             r 4  
             g' 4  
             r 2  
             \bar "|"  %{ end measure 21 %} 
             cis'' 4  
             r 4.  
             a' 8  
             r 2  
             \bar "|"  %{ end measure 22 %} 
             d' 8  
             r 2  
             e' 4  
             r 4.  
             \bar "|"  %{ end measure 23 %} 
             fis' 2  ~  
             fis' 8  
             r 16  
             d' 16  
             r 2  
             \bar "|"  %{ end measure 24 %} 
             d'' 4  
             r 4.  
             d'' 8  
             r 2  
             \bar "|"  %{ end measure 25 %} 
             e'' 8  
             r 2  
             e'' 4  
             r 4.  
             \bar "|"  %{ end measure 26 %} 
             fis' 2  ~  
             fis' 8  
             r 16  
             b' 16  
             r 2  
             \bar "|"  %{ end measure 27 %} 
             cis'' 4  
             r 4  
             a' 4  
             r 2  
             \bar "|"  %{ end measure 28 %} 
             d' 4  
             r 4.  
             d' 8  
             r 2  
             \bar "|"  %{ end measure 29 %} 
             g' 8  
             r 2  
             e' 4  
             r 4.  
             \bar "|"  %{ end measure 30 %} 
             g' 4  
             r 4  
             gis' 4  
             r 2  
             \bar "|"  %{ end measure 31 %} 
             b' 4  
             r 4.  
             g' 8  
             r 2  
             \bar "|"  %{ end measure 32 %} 
             g' 2  
             r 8  
             e' 4.  
             r 4  
             \bar "|"  %{ end measure 33 %} 
             fis'' 2  
             r 4  
             fis'' 4.  
             r 8  
             \bar "|"  %{ end measure 34 %} 
             fis' 4.  
             r 8  
             fis' 2  
             r 4  
             \bar "|"  %{ end measure 35 %} 
             b' 2  
             r 8  
             fis' 4.  
             r 4  
             \bar "|"  %{ end measure 36 %} 
             cis'' 4.  
             r 8  
             a' 2  
             r 4  
             \bar "|"  %{ end measure 37 %} 
             d'' 2  
             r 8  
             b' 4.  
             r 4  
             \bar "|"  %{ end measure 38 %} 
             e' 2  
             r 4  
             d'' 4.  
             r 8  
             \bar "|"  %{ end measure 39 %} 
             a' 4.  
             r 8  
             fis' 2  
             r 4  
             \bar "|"  %{ end measure 40 %} 
             e'' 2  
             r 8  
             e'' 4.  
             r 4  
             \bar "|"  %{ end measure 41 %} 
             d'' 2  
             r 4  
             d'' 4.  
             r 8  
             \bar "|"  %{ end measure 42 %} 
             b' 2  
             r 8  
             e' 4.  
             r 4  
             \bar "|"  %{ end measure 43 %} 
             e' 2  
             r 4  
             e' 4.  
             r 8  
             \bar "|"  %{ end measure 44 %} 
             a' 4.  
             r 8  
             g' 2  
             r 4  
             \bar "|"  %{ end measure 45 %} 
             b' 2  
             r 8  
             a' 4.  
             r 4  
             \bar "|"  %{ end measure 46 %} 
             fis' 2  
             r 4  
             fis' 4.  
             r 8  
             \bar "|"  %{ end measure 47 %} 
             fis' 4.  
             r 8  
             d' 2  
             r 4  
             \bar "|"  %{ end measure 48 %} 
             d'' 4  
             r 2  
             fis' 4  
             r 4  
             \bar "|"  %{ end measure 49 %} 
             e'' 4.  
             r 4  
             g' 4.  
             r 4  
             \bar "|"  %{ end measure 50 %} 
             a 2  
             r 4  
             a' 4  
             r 4  
             \bar "|"  %{ end measure 51 %} 
             a' 4  
             r 2  
             cis' 4  
             r 4  
             \bar "|"  %{ end measure 52 %} 
             cis'' 4.  
             r 4  
             fis' 4.  
             r 4  
             \bar "|"  %{ end measure 53 %} 
             d'' 2  
             r 4  
             d' 4  
             r 4  
             \bar "|"  %{ end measure 54 %} 
             a 4.  
             r 4  
             a' 4.  
             r 4  
             \bar "|"  %{ end measure 55 %} 
             a' 2  
             r 4  
             a 4  
             r 4  
             \bar "|"  %{ end measure 56 %} 
             b' 4  
             r 2  
             gis' 4  
             r 4  
             \bar "|"  %{ end measure 57 %} 
             a' 4.  
             r 4  
             fis' 4.  
             r 4  
             \bar "|"  %{ end measure 58 %} 
             a 2  
             r 4  
             a' 4  
             r 4  
             \bar "|"  %{ end measure 59 %} 
             cis'' 4  
             r 2  
             e' 4  
             r 4  
             \bar "|"  %{ end measure 60 %} 
             a' 4  
             r 2  
             fis' 8  
             r 4.  
             \bar "|"  %{ end measure 61 %} 
             b' 4.  
             r 4  
             g' 8  
             r 2  
             \bar "|"  %{ end measure 62 %} 
             a' 2  
             r 8  
             d' 4.  
             r 4  
             \bar "|"  %{ end measure 63 %} 
             fis' 4  
             r 2  
             a 8  
             r 4.  
             \bar "|"  %{ end measure 64 %} 
             b' 4.  
             r 4  
             d' 8  
             r 2  
             \bar "|"  %{ end measure 65 %} 
             g' 2  
             r 8  
             e' 4.  
             r 4  
             \bar "|"  %{ end measure 66 %} 
             a' 4.  
             r 4  
             d' 8  
             r 2  
             \bar "|"  %{ end measure 67 %} 
             b' 2  
             r 8  
             b' 4.  
             r 4  
             \bar "|"  %{ end measure 68 %} 
             e'' 4  
             r 2  
             e'' 8  
             r 4.  
             \bar "|"  %{ end measure 69 %} 
             d'' 4.  
             r 4  
             d'' 8  
             r 2  
             \bar "|"  %{ end measure 70 %} 
             a' 2  
             r 8  
             d' 4.  
             r 4  
             \bar "|"  %{ end measure 71 %} 
             b' 4  
             r 2  
             b' 8  
             r 4.  
             \bar "|"  %{ end measure 72 %} 
             r 1  
             s 4  
             \bar "|"  %{ end measure 73 %} 
             r 1  
             s 4  
             \bar "|"  %{ end measure 74 %} 
             r 1  
             s 4  
             \bar "|"  %{ end measure 75 %} 
             r 1  
             s 4  
             \bar "|"  %{ end measure 76 %} 
             a' 2.  
             r 2  
             \bar "|"  %{ end measure 77 %} 
             b' 2  
             r 2.  
             \bar "|"  %{ end measure 78 %} 
             d' 4  
             r 1  
             \bar "|"  %{ end measure 79 %} 
             e' 2.  
             r 2  
             r 4  
             \bar "|"  %{ end measure 80 %} 
             fis' 2  
             r 2  
             r 4  
             r 2.  
             \bar "|"  %{ end measure 81 %} 
             r 1  
             s 4  
             \bar "|"  %{ end measure 82 %} 
             r 1  
             s 4  
             \bar "|"  %{ end measure 83 %} 
             r 1  
             s 4  
             \bar "|"  %{ end measure 84 %} 
             r 1  
             s 4  
             \bar "|"  %{ end measure 85 %} 
             r 1  
             s 4  
             \bar "|"  %{ end measure 86 %} 
             r 1  
             s 4  
             \bar "|"  %{ end measure 87 %} 
             r 1  
             s 4  
             \bar "|"  %{ end measure 88 %} 
              } 
            
 
        >>
      
  } 
 
\paper { }
\layout {
  \context {
    \RemoveEmptyStaffContext
    \override VerticalAxisGroup #'remove-first = ##t
  }
 }
 
