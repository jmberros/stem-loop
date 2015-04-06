class Utils
  def time_in_words(seconds)
    mm, ss = seconds.divmod(60)
    hh, mm = mm.divmod(60)
    dd, hh = hh.divmod(24)

    in_words = ""
    in_words += "#{dd} days, " if dd > 0
    in_words += "#{hh} hours, " if hh > 0
    in_words += "#{mm} minutes, " if mm > 0
    in_words += "#{ss} seconds"

    in_words
  end
end
