# Todo AI Chatbot - Troubleshooting Guide

## Common Issues and Solutions

### Chat Interface Not Opening
**Problem**: The floating chat icon doesn't respond when clicked
**Solutions**:
- Refresh the page to reload JavaScript
- Clear browser cache and cookies
- Check browser console for JavaScript errors
- Ensure you're using a supported browser (Chrome, Firefox, Safari, Edge)

### AI Not Responding to Requests
**Problem**: The AI doesn't seem to understand or respond to natural language requests
**Solutions**:
- Try simpler, more direct language (e.g., "Add task: buy groceries" instead of "Could you possibly add a task for me to buy groceries?")
- Be specific about the action you want (add, list, update, complete, delete)
- Include task IDs when referencing specific tasks
- Check that you have a stable internet connection

### Tasks Not Appearing After AI Action
**Problem**: Tasks created or modified via chat don't appear in the main task list
**Solutions**:
- Refresh the dashboard page to sync with the latest changes
- Check that the AI confirmed the action was successful
- Verify you're logged into the correct account
- Look for any error messages in the chat interface

### Authentication Issues
**Problem**: Receiving "Authentication required" or "Access denied" errors
**Solutions**:
- Verify you're logged in to your account
- Try logging out and logging back in
- Check that your session hasn't expired
- Clear browser cookies and log in again

### Slow Response Times
**Problem**: The AI takes a long time to respond to requests
**Solutions**:
- Check your internet connection speed
- The Cohere API may be experiencing high load
- Try again during off-peak hours
- Restart your browser if it's been running for a long time

### Task Access Issues
**Problem**: Unable to access or modify tasks that belong to you
**Solutions**:
- Verify that you're logged in to the correct account
- Check that the task IDs you're referencing are correct
- The task may have been deleted by another session
- Try listing all tasks to see the current list

## Advanced Troubleshooting

### Checking API Connectivity
1. Open browser developer tools (F12)
2. Go to the Network tab
3. Perform a chat action
4. Look for API calls to `/api/chat`
5. Check the response status and any error messages

### Verifying Authentication Headers
1. In Network tab, examine the `/api/chat` request
2. Verify the Authorization header contains a valid JWT token
3. Check that the token hasn't expired

### Database Connection Issues
**Symptoms**: All chat functionality fails with server errors
**Solutions**:
- Contact system administrator
- Check backend server logs
- Verify database connection is available
- Confirm environment variables are set correctly

## Error Messages and Meanings

### "Task does not belong to the authenticated user"
- **Meaning**: Attempting to access or modify a task that belongs to another user
- **Solution**: Verify the task ID is correct and belongs to your account

### "Invalid input parameters"
- **Meaning**: The AI extracted incorrect parameters from your request
- **Solution**: Rephrase your request using clearer language

### "Conversation not found or access denied"
- **Meaning**: Attempting to access a conversation that doesn't exist or isn't yours
- **Solution**: Start a new conversation or verify the conversation ID

### "Failed to add task: Title must be between 1 and 200 characters"
- **Meaning**: The task title exceeds length limits
- **Solution**: Use a shorter task title

## When to Contact Support

Contact support if you experience:
- Persistent authentication failures
- Consistent API errors across multiple requests
- Data integrity issues (tasks disappearing, incorrect ownership)
- Performance issues lasting more than a few hours
- Security concerns or suspicious activity

## Support Information

When contacting support, please provide:
- Your account email
- Browser and version
- Specific error messages received
- Steps to reproduce the issue
- Screenshot of any error messages (if applicable)