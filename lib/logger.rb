class Logger
  def debug(message)
    puts message if $stdout.tty? # Doesn't print help messages when piping
    # FIXME ^ This should only write to STDOUT if ENV['DEBUG']
  end
end
