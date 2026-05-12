# Skill: Supabase

## Use This Skill When

Working on database schema or Supabase integration.

## Tables

- system_config
- event_logs
- device_commands
- command_results

## Rules

- Do not expose service role key to client.
- Use server-side API routes for privileged writes.
- Add indexes for common queries.
- Keep command queue simple.
- Update DATABASE_SCHEMA.md after changes.

## Command Statuses

- pending
- processing
- done
- failed
