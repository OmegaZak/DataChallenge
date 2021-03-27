    df['Day'] = df['Time'].dt.to_period('D')
     df['Month'] = df['Time'].dt.to_period('M')
     df['Year'] = df['Time'].dt.to_period('Y')
     df['Hour'] = df['Time'].dt.to_period('H')
     df['Minute'] = df['Time'].dt.to_period('Min') 

    
    
    df['Day'] = df['Time'].dt.day
    df['Month'] = df['Time'].dt.month
    df['Year'] = df['Time'].dt.year
    df['Hour'] = df['Time'].dt.hour
    df['Minute'] = df['Time'].dt.minute
